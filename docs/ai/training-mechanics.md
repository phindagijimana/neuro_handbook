# Training mechanics

> How to actually train a 3D medical-imaging model on a GPU cluster — mixed precision, checkpointing, multi-GPU, OOM debugging, profiling. The engineering layer underneath every successful run.

This chapter assumes you have a working PyTorch + MONAI environment. See [Computing → Python scientific stack](../computing/python-stack.md) and [GPUs and accelerators](../computing/gpus.md) first.

## A canonical training loop in MONAI

```python
import torch, monai
from monai.data import DataLoader, CacheDataset
from monai.networks.nets import UNet
from monai.losses import DiceCELoss
from monai.metrics import DiceMetric
from monai.transforms import (Compose, LoadImaged, ScaleIntensityRanged,
                              RandCropByPosNegLabeld, RandFlipd, ToTensord)

# 1. Transforms (deterministic part of preprocessing inside the dataloader)
train_tfm = Compose([
    LoadImaged(keys=["image", "label"]),
    ScaleIntensityRanged(keys="image", a_min=0, a_max=2000, b_min=0, b_max=1, clip=True),
    RandCropByPosNegLabeld(keys=["image", "label"], label_key="label",
                            spatial_size=(96, 96, 96), pos=1, neg=1, num_samples=4),
    RandFlipd(keys=["image", "label"], spatial_axis=[0], prob=0.5),
    ToTensord(keys=["image", "label"]),
])

train_ds = CacheDataset(data=train_records, transform=train_tfm, cache_rate=0.5)
train_loader = DataLoader(train_ds, batch_size=2, shuffle=True, num_workers=4,
                          pin_memory=True)

# 2. Model + loss + optimiser
device = torch.device("cuda")
model = UNet(spatial_dims=3, in_channels=1, out_channels=2,
             channels=(16, 32, 64, 128, 256), strides=(2, 2, 2, 2)).to(device)
loss_fn = DiceCELoss(softmax=True, to_onehot_y=True)
opt = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
scaler = torch.amp.GradScaler("cuda")

# 3. The loop
for epoch in range(200):
    model.train()
    for batch in train_loader:
        x = batch["image"].to(device, non_blocking=True)
        y = batch["label"].to(device, non_blocking=True)

        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            pred = model(x)
            loss = loss_fn(pred, y)

        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.step(opt)
        scaler.update()
```

Below: what each block does and how to scale it.

## Mixed precision

Modern GPUs (A100, H100, RTX 30/40-series) accelerate `bfloat16` 2-4× over `float32`. Memory drops too.

- **A100 / H100 →** `bfloat16` (preferred; wider dynamic range, no loss scaling needed).
- **V100 / RTX 20-series →** `float16` (use `GradScaler`).
- Always benchmark; sometimes `float16` is still faster than `bfloat16` on Volta-class GPUs.

Wrap the **forward + loss** in `autocast`; keep the **backward** outside.

## Patch sampling — the secret to 3D training

A 256³ volume on a 24 GB GPU is impossible; an 80³ patch is fine. MONAI's `RandCropByPosNegLabeld` does foreground-balanced sampling so each batch contains lesion voxels.

Rule of thumb:

- Patch size ≈ `(96, 96, 96)` for general segmentation; `(64, 64, 64)` for tight memory.
- `num_samples=4` per case in the cropping transform: amplifies the effective batch size.
- Always include at least one foreground patch per class per batch.

## Gradient accumulation — bigger effective batch

When you need a batch of 16 but the GPU fits 2, accumulate:

```python
ACCUM = 8
for step, batch in enumerate(train_loader):
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        loss = loss_fn(model(batch["image"].to(device)), batch["label"].to(device))
    scaler.scale(loss / ACCUM).backward()
    if (step + 1) % ACCUM == 0:
        scaler.step(opt); scaler.update()
        opt.zero_grad(set_to_none=True)
```

## Multi-GPU — distributed data parallel

```python
import torch.distributed as dist
import torch.multiprocessing as mp

def setup(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def train(rank, world_size):
    setup(rank, world_size)
    model = UNet(...).to(rank)
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank])
    sampler = torch.utils.data.distributed.DistributedSampler(
        train_ds, num_replicas=world_size, rank=rank, shuffle=True)
    loader = DataLoader(train_ds, batch_size=2, sampler=sampler, num_workers=4)
    # ... training loop with sampler.set_epoch(epoch) at top
    dist.destroy_process_group()

mp.spawn(train, args=(4,), nprocs=4)
```

Even simpler: use [`accelerate`](https://huggingface.co/docs/accelerate/):

```bash
accelerate config       # one-time
accelerate launch train.py
```

`accelerate` wraps DDP, mixed precision, gradient accumulation, and distributed sampling behind a small API.

## Checkpointing and resume

```python
ckpt_path = "checkpoints/last.pt"

def save_ckpt(epoch):
    torch.save({"epoch": epoch,
                "model": model.state_dict(),
                "opt": opt.state_dict(),
                "scaler": scaler.state_dict()},
               ckpt_path)

def load_ckpt():
    if Path(ckpt_path).exists():
        ck = torch.load(ckpt_path, map_location=device, weights_only=True)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        scaler.load_state_dict(ck["scaler"])
        return ck["epoch"] + 1
    return 0
```

On clusters with pre-emption (spot, Slurm requeue), checkpoint *every epoch*. The cost is minimal; the cost of redoing 24 h is not.

## GPU memory profiling and debugging

Before the OOM hits, it helps to know what each component of training is actually costing you. The recipes above assume you already have a sense of the bill; this section makes that bill explicit.

### What lives on the GPU during training

Four things compete for VRAM during a forward + backward pass:

| Component | Size in fp32 | Size in fp16/bf16 | Notes |
| --- | --- | --- | --- |
| **Model parameters** | `N × 4` bytes | `N × 2` bytes | `N` = parameter count |
| **Gradients** | `N × 4` bytes | `N × 2` bytes | One per parameter, allocated on `.backward()` |
| **Optimiser state** | `N × 8` bytes (Adam) | `N × 8` bytes (Adam in fp32 master) | Adam keeps `m` and `v`; SGD-momentum keeps one buffer |
| **Activations** | proportional to `B × C × H × W × D × bytes_per_elem` | half that | Saved for backward; this is where 3D models hurt |

Worked example — a 3D U-Net with ~5M parameters, batch size 2, patch `96³`, base channel 32:

- Params (bf16): `5e6 × 2  ≈ 10 MB`
- Grads  (bf16): `5e6 × 2  ≈ 10 MB`
- Adam state (fp32 master copies of `m`, `v`, and an fp32 weight shadow): `5e6 × 12 ≈ 60 MB`
- Activations (dominant cost): each encoder block holds a tensor of shape `[2, C, 96/s, 96/s, 96/s]`. The first block alone is `2 × 32 × 96³ × 2 bytes ≈ 113 MB`. Sum across ~10 saved tensors → **~1–2 GB**.

Total: roughly **2–3 GB** for a small U-Net at `96³`. Double the patch to `128³` and activations grow `(128/96)³ ≈ 2.4×`. Triple-check that intuition before you blame [`torch.cuda`](https://docs.pytorch.org/docs/stable/cuda.html) for misbehaving — usually it's geometry.

### Mixed-precision gotchas

[`fp16`](https://docs.pytorch.org/docs/stable/amp.html) has a narrow exponent range (max ~65 504). Gradients can underflow to zero or overflow to `inf`; that's why `torch.amp.GradScaler` multiplies the loss by a large factor before backward and divides it back before the optimiser step. `GradScaler.update()` halves the scale every time it sees an `inf`/`NaN` gradient, and doubles it after a few clean steps. Two bugs to watch for:

- **NaN losses immediately after `scaler.update()`** — the scale has collapsed to 1 (or below). Either your loss is genuinely diverging, or you're mixing precisions inside the optimiser state. Print `scaler.get_scale()` every step until you see the pattern.
- **Optimiser state silently in fp16** — if you build the optimiser *after* casting the model to half precision, Adam's `m` and `v` will be fp16 and lose accumulator resolution. Always keep optimiser state in fp32 (the default in [`torch.cuda.amp`](https://docs.pytorch.org/docs/stable/amp.html) and `accelerate`).

[`bfloat16`](https://docs.pytorch.org/docs/stable/tensors.html#torch.bfloat16) has the same exponent range as fp32 (8 bits) but only 7 mantissa bits. No loss scaling needed; just `autocast(dtype=torch.bfloat16)` and go. Prefer it on A100/H100/RTX 30+.

### Profiling commands

The everyday toolbox:

- **[`nvidia-smi`](https://developer.nvidia.com/nvidia-system-management-interface)** — board-level view of utilisation and memory: `nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv -l 1`.
- **[`torch.cuda.memory_allocated()`](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory_allocated.html)** / **`memory_reserved()`** — what PyTorch currently holds and what it has cached from the allocator.
- **[`torch.cuda.max_memory_allocated()`](https://docs.pytorch.org/docs/stable/generated/torch.cuda.max_memory_allocated.html)** + **`reset_peak_memory_stats()`** — the peak between two checkpoints. This is the number you actually care about.
- **[`torch.cuda.memory_summary()`](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory_summary.html)** — a long-form dump of allocator buckets; useful when fragmentation is suspected.
- **[`torch.profiler`](https://docs.pytorch.org/docs/stable/profiler.html)** — see the existing Profiling section below for a full trace.

A 12-line probe you can drop around a forward + backward:

```python
import torch

torch.cuda.reset_peak_memory_stats()
x = batch["image"].to(device, non_blocking=True)
y = batch["label"].to(device, non_blocking=True)

with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    pred = model(x)
    loss = loss_fn(pred, y)
loss.backward()

print(f"peak alloc: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")
print(f"reserved:   {torch.cuda.memory_reserved()      / 1e9:.2f} GB")
```

Run this once at the start of training, log the numbers, and compare against the table above.

### Common bugs

- **"Memory leak in the [`DataLoader`](https://docs.pytorch.org/docs/stable/data.html)"** — workers retain CUDA tensors across iterations when `persistent_workers=True` is combined with code that accidentally moves data to GPU inside the worker. Keep `.to(device)` in the main process; set `pin_memory=True` to get fast host→device copies; only enable `persistent_workers=True` if your dataset construction is genuinely expensive.
- **Activation memory grows with depth** — encoder-decoder nets save every skip-connection tensor for backward. Wrap heavy blocks in [`torch.utils.checkpoint`](https://docs.pytorch.org/docs/stable/checkpoint.html) to trade compute for memory; activations are recomputed during backward.
- **Peak memory fine at step 1, OOM at step 100** — allocator fragmentation. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` ([docs](https://docs.pytorch.org/docs/stable/notes/cuda.html#memory-management)) before launching Python; the allocator will grow segments instead of carving fixed-size blocks.
- **Optimiser step OOMs but forward fits** — Adam allocates `m` and `v` lazily on the first `.step()`. Account for the extra `2 × N × 4` bytes when sizing the run.

### Rule-of-thumb table

For a 3D U-Net with `~5M` params, channel base 32, bf16 + Adam:

| Patch | Batch | Approx. VRAM | Fits on |
| --- | --- | --- | --- |
| `64³` | 2 | ~1.5 GB | anything ≥ 8 GB |
| `96³` | 2 | ~3 GB | RTX 3080 (10 GB) |
| `96³` | 4 | ~5 GB | RTX 3090 / A4000 |
| `128³` | 2 | ~7 GB | RTX 3090 (24 GB) |
| `160³` | 2 | ~13 GB | A100 (40 GB) |
| `192³` | 2 | ~22 GB | A100 (40 GB) |

Numbers double for fp32, halve again if you turn on `torch.utils.checkpoint` everywhere. They are starting points, not contracts — always measure on your own model with the probe above.

## OOM debugging — the loop

When you see `RuntimeError: CUDA out of memory`:

1. **Print everything.** `print(model)`, `print(x.shape)`, `torch.cuda.memory_allocated() / 1e9`.
2. **Reduce.** Halve the patch size; halve the batch size; halve `num_workers`.
3. **Switch to bfloat16.**
4. **Enable gradient checkpointing** (`monai.networks.nets.UNet` supports it via custom wrapping):

```python
import torch.utils.checkpoint as cp
# rewrite forward with cp.checkpoint on the heavy blocks
```

5. **`torch.cuda.empty_cache()`** between epochs (rarely the actual fix).
6. **Profile** with `torch.profiler` to find the actual peak-memory operation.

## Profiling

```python
from torch.profiler import profile, record_function, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
             schedule=torch.profiler.schedule(wait=1, warmup=1, active=3),
             record_shapes=True, with_stack=True) as prof:
    for step, batch in enumerate(loader):
        with record_function("forward"):
            out = model(batch["image"].to(device))
        with record_function("backward"):
            loss = loss_fn(out, batch["label"].to(device))
            loss.backward(); opt.step(); opt.zero_grad()
        prof.step()
        if step >= 5: break

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=20))
```

A well-tuned 3D U-Net runs at >80% GPU utilisation. Below 50% the bottleneck is usually data loading: increase `num_workers`, switch to a faster format (HDF5 / Zarr), or cache more aggressively.

## Learning-rate scheduling

- **Warmup** for the first 1-5k steps prevents early divergence on 3D nets.
- **Cosine decay** to 0 over the full schedule is the modern default.
- **OneCycle** ([Smith 2017](https://doi.org/10.48550/arXiv.1708.07120)) — peak LR + decay; converges fast.

```python
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=len(loader)*200)
```

## Reproducibility checklist

- [ ] `torch.manual_seed(42)`, `np.random.seed(42)`, `random.seed(42)`.
- [ ] `torch.backends.cudnn.deterministic = True` (slower but reproducible).
- [ ] Save dataset / split metadata alongside the checkpoint.
- [ ] Pin Python, PyTorch, CUDA, MONAI versions in a lockfile.
- [ ] Log to Weights & Biases / MLflow / TensorBoard — the *experiment* is metadata, not just the weights.

## References

1. **Cardoso MJ, Li W, Brown R, et al.** MONAI. *arXiv:2211.02701.* 2022. [doi:10.48550/arXiv.2211.02701](https://doi.org/10.48550/arXiv.2211.02701)
2. **Smith LN.** Super-convergence: very fast training of neural networks using large learning rates. *arXiv:1708.07120.* 2017. [doi:10.48550/arXiv.1708.07120](https://doi.org/10.48550/arXiv.1708.07120)
3. **Loshchilov I, Hutter F.** Decoupled weight decay regularization (AdamW). *ICLR.* 2019. [arXiv:1711.05101](https://doi.org/10.48550/arXiv.1711.05101)
4. **Dao T, Fu DY, Ermon S, et al.** FlashAttention. *NeurIPS.* 2022. [arXiv:2205.14135](https://doi.org/10.48550/arXiv.2205.14135)
5. **Goyal P, Dollár P, Girshick R, et al.** Accurate, large minibatch SGD: training ImageNet in 1 hour. *arXiv:1706.02677.* 2017. [doi:10.48550/arXiv.1706.02677](https://doi.org/10.48550/arXiv.1706.02677)
6. **Micikevicius P, Narang S, Alben J, et al.** Mixed precision training. *ICLR.* 2018. [arXiv:1710.03740](https://doi.org/10.48550/arXiv.1710.03740)
7. **Chen T, Xu B, Zhang C, Guestrin C.** Training deep nets with sublinear memory cost. *arXiv:1604.06174.* 2016. [doi:10.48550/arXiv.1604.06174](https://doi.org/10.48550/arXiv.1604.06174) — the gradient-checkpointing paper.
8. **PyTorch.** [CUDA semantics — memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html#memory-management); [autograd profiler](https://docs.pytorch.org/docs/stable/profiler.html); [`torch.cuda` memory APIs](https://docs.pytorch.org/docs/stable/cuda.html#memory-management).
9. **NVIDIA.** [`nvidia-smi` reference](https://developer.nvidia.com/nvidia-system-management-interface) and [NVML query keys](https://docs.nvidia.com/deploy/nvml-api/).

## Where to next

[Foundation models](foundation-models.md) — when training from scratch isn't the right choice.
