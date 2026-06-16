# Deep learning for imaging

> Architectures and training tricks for when the input is voxels.

If your task is segmentation, lesion detection, image-to-image translation, or anything where the *spatial structure* of the image matters, deep learning is the default. This chapter covers the parts that are different from generic computer vision.

## 2D vs 2.5D vs 3D

| Approach | Pro | Con |
| --- | --- | --- |
| **2D** (slice-by-slice) | Cheap, leverages 2D pre-training | Ignores out-of-plane context |
| **2.5D** (3 orthogonal slices through the voxel) | Cheap + some context | Asymmetric receptive field |
| **3D** (volume) | True spatial context | Memory-hungry; rarely pre-trained |

A common pattern: a 2.5D model on full volumes for rough localisation, then a 3D model on cropped patches around regions of interest.

## Segmentation: U-Net and its descendants

The 3D U-Net is the workhorse for medical segmentation. Skip connections preserve fine detail; the bottleneck enforces context.

**nnU-Net** is the reference implementation — it auto-configures architecture, patch size, normalisation, and training schedule from the dataset. Start there. Beat it before you build your own.

## Volume transformers

For larger datasets and richer tasks (multi-class segmentation, captioning), transformer-based architectures (Swin UNETR, UNETR, MedSegMamba) are now competitive with — and often beat — pure CNN U-Nets.

Key idea: tokenise the volume into patches, attend across patches, decode back to voxel space. Memory cost is quadratic in number of tokens, so patch size and stride matter enormously.

## Training tricks that actually matter

- **Patch sampling.** Brains are mostly background. Sampling patches uniformly wastes compute. Use class-balanced or foreground-biased sampling.
- **Class imbalance loss.** Cross-entropy is dominated by background. Combine with Dice (`DiceCE`, `Focal`, `Tversky`).
- **3D augmentation.** Rotations and flips must respect anatomy (don't flip left/right unless the task is symmetric). Elastic deformations help; intensity augmentation (bias field, Gaussian noise) helps more than you'd think.
- **Mixed precision.** `torch.autocast` cuts memory ~40% with no accuracy hit. Always on.
- **Gradient accumulation.** When a single 3D patch fills the GPU, accumulate gradients over multiple patches before stepping the optimiser.
- **Sliding-window inference.** At test time, run the model on overlapping patches and average the predictions. MONAI's `sliding_window_inference` handles this.

## A minimal MONAI training loop

```python
import torch
from monai.data import DataLoader, Dataset
from monai.networks.nets import UNet
from monai.losses import DiceCELoss
from monai.transforms import Compose, LoadImaged, RandFlipd, ScaleIntensityd, ToTensord

transforms = Compose([
    LoadImaged(keys=["image", "label"]),
    ScaleIntensityd(keys="image"),
    RandFlipd(keys=["image", "label"], spatial_axis=0, prob=0.5),
    ToTensord(keys=["image", "label"]),
])

dataset = Dataset(data=train_records, transform=transforms)
loader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=4)

model = UNet(
    spatial_dims=3,
    in_channels=1,
    out_channels=4,
    channels=(16, 32, 64, 128, 256),
    strides=(2, 2, 2, 2),
).cuda()

loss_fn = DiceCELoss(softmax=True, to_onehot_y=True)
opt = torch.optim.AdamW(model.parameters(), lr=1e-4)

for batch in loader:
    x = batch["image"].cuda()
    y = batch["label"].cuda()
    with torch.autocast(device_type="cuda"):
        pred = model(x)
        loss = loss_fn(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
```

This is intentionally simple. Real production code adds checkpointing, AMP scaling, distributed training, and learning-rate schedules — but the skeleton above is enough to *understand* what's happening.

## Where to next

[Foundation models](foundation-models.md) — when even your custom architecture isn't enough and you need to stand on someone else's pre-training.
