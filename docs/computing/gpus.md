# GPUs and accelerators

> CUDA versions, instance types, and the small mistakes that waste hours of paid GPU time.

## What you actually need

- **A modern NVIDIA GPU** (A100, H100, L4, RTX 4090). AMD's ROCm is improving but PyTorch / MONAI / nnU-Net are still NVIDIA-first.
- **CUDA toolkit** matching what your framework was built against.
- **cuDNN** matching CUDA.
- **PyTorch / TensorFlow** built against the same CUDA version.

The PyTorch install commands at <https://pytorch.org/get-started/locally/> include the right CUDA wheel for each combo. Use them instead of guessing.

## Picking a cloud instance

| Workload | Instance |
| --- | --- |
| Inference / small fine-tune | T4, L4 |
| 3D U-Net training | A100 40 GB or 80 GB |
| Foundation-model training | A100 80 GB ×8 or H100 ×8 |
| Quick prototyping | RTX 4090 on a workstation |

A100 80 GB is the workhorse — large enough for 3D patches, fast enough to iterate, available everywhere.

## Multi-GPU patterns

- **Data parallelism** — same model, different batches per GPU. PyTorch's `torch.nn.parallel.DistributedDataParallel` is the right primitive. `accelerate` wraps it nicely.
- **Model parallelism** — model split across GPUs. Only worth it when one GPU cannot hold the model.
- **Pipeline parallelism** — different layers on different GPUs. Niche; consider only at very large scale.

For neuroimaging, data parallelism on 2–8 GPUs covers ~95% of training workloads.

## Memory tricks

- **Mixed precision** — `bf16` on A100/H100, `fp16` elsewhere. 1.5–2× memory savings.
- **Gradient checkpointing** — recompute activations during backward instead of storing them. ~50% memory at the cost of ~25% compute.
- **Gradient accumulation** — small effective batch with logical large batch. Same as one GPU + accumulation steps.
- **Smaller patches** — for 3D segmentation, 96³ → 64³ patches halves memory.

## The CUDA-OOM debugging loop

When you see `RuntimeError: CUDA out of memory`:

1. **Print the model size** (`sum(p.numel() for p in model.parameters())`) — is it sane?
2. **Print the input tensor size** — are you feeding a 256³ volume when you meant 64³?
3. **`torch.cuda.empty_cache()`** between epochs (rarely fixes the root cause, often hides it).
4. **Profile with `torch.profiler`** to find the actual peak-memory operation.

## When something looks "slow"

- Check if you're actually using the GPU (`nvidia-smi` while training).
- Check that data loading isn't the bottleneck (`num_workers` in DataLoader; pre-cache disk reads).
- Check mixed precision is on.
- Check the model isn't pinned to one device while data sits on another.

A well-tuned 3D U-Net trains at > 80% GPU utilisation. Anything below 50% has a fixable problem.

## Where to next

[Editor and IDE setup](editor.md) — the small ergonomic wins.
