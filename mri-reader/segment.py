"""Apply a compatible trained binary segmentation model to a 3D NIfTI."""
import argparse
import nibabel as nib
import numpy as np
import torch
from monai.inferers import sliding_window_inference


def segment(source, model_path, destination):
    image = nib.as_closest_canonical(nib.load(source))
    values = image.get_fdata(dtype=np.float32)
    if values.ndim != 3 or not np.isfinite(values).all():
        raise ValueError("Expected a finite 3D volume.")
    tissue = values != 0
    if not tissue.any():
        raise ValueError("Empty foreground.")
    signal = values[tissue]
    values[tissue] = (signal - signal.mean()) / max(float(signal.std()), 1e-6)
    model = torch.jit.load(model_path, map_location="cpu").eval()
    with torch.inference_mode():
        logits = sliding_window_inference(torch.from_numpy(values)[None, None],
            (96, 96, 96), 1, model, overlap=0.25)
    if logits.shape != (1, 1, *values.shape) or not logits.isfinite().all():
        raise ValueError("Model must return one finite binary logit per voxel.")
    mask = (logits[0, 0].numpy() > 0).astype(np.uint8)
    nib.save(nib.Nifti1Image(mask, image.affine), destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("model", help="Trusted trained TorchScript model")
    parser.add_argument("destination")
    args = parser.parse_args()
    segment(args.source, args.model, args.destination)
