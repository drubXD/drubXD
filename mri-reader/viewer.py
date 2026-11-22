"""Export a scrollable grayscale slice viewer to a self-contained HTML file."""
import argparse
import base64
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image


def volume(path):
    if path is None:
        z, y, x = np.ogrid[-1:1:48j, -1:1:96j, -1:1:96j]
        return np.exp(-4 * (x*x + y*y + z*z))  # Synthetic intensity phantom
    name = path.name.lower()
    if name.endswith((".nii", ".nii.gz")):
        import nibabel as nib
        img = nib.as_closest_canonical(nib.load(path))
        if len(img.shape) != 3:
            raise ValueError("Select a single 3D NIfTI volume.")
        return img.get_fdata(dtype=np.float32).transpose(2, 1, 0)[:, ::-1, :]
    if name.endswith(".dcm"):
        import pydicom
        ds = pydicom.dcmread(path)
        if ds.SamplesPerPixel != 1:
            raise ValueError("Select a grayscale DICOM image.")
        data = ds.pixel_array.astype(float) * float(getattr(ds, "RescaleSlope", 1))
        data += float(getattr(ds, "RescaleIntercept", 0))
        if ds.PhotometricInterpretation == "MONOCHROME1":
            data = -data
        return data.reshape((-1, ds.Rows, ds.Columns))
    with Image.open(path) as image:
        return np.asarray(image.convert("L"))[None, :, :]


def export(data, output):
    finite = np.isfinite(data)
    if not finite.any():
        raise ValueError("No finite image intensities.")
    low, high = np.percentile(data[finite], [1, 99])
    if high <= low:
        low, high = data[finite].min(), data[finite].max()
    frames = []
    for plane in data:
        scaled = (np.nan_to_num(plane, nan=low) - low) / max(float(high-low), 1e-10)
        image = Image.fromarray((255 * np.clip(scaled, 0, 1)).astype("uint8"))
        buffer = io.BytesIO()
        image.save(buffer, "PNG")
        frames.append(base64.b64encode(buffer.getvalue()).decode("ascii"))
    template = Path(__file__).with_name("viewer.html").read_text(encoding="utf8")
    output.write_text(template.replace("/*FRAMES*/[]", json.dumps(frames)), encoding="utf8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="Omit to generate a synthetic phantom")
    parser.add_argument("--out", type=Path, default=Path("scan.html"))
    args = parser.parse_args()
    export(volume(args.input), args.out)
    print(args.out.resolve())
