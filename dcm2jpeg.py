#!/usr/bin/env python3
"""Convert all DICOM (.dcm) files in a directory tree to JPEG."""

import argparse
import sys
from pathlib import Path

import numpy as np
import pydicom
from PIL import Image


def _get_dicom_value(attr: object) -> float:
    """Extract a scalar from a DICOM attribute (may be MultiValue)."""
    if isinstance(attr, (pydicom.multival.MultiValue, list)):
        return float(attr[0])
    return float(attr)  # type: ignore[arg-type]


def apply_windowing(
    pixel_array: np.ndarray,
    ds: pydicom.Dataset,
) -> np.ndarray:
    """Apply DICOM windowing to normalize pixel values to 0-255."""
    if hasattr(ds, "WindowCenter") and hasattr(ds, "WindowWidth"):
        center = _get_dicom_value(ds.WindowCenter)
        width = _get_dicom_value(ds.WindowWidth)
        lower = center - width / 2
        upper = center + width / 2
        pixel_array = np.clip(pixel_array, lower, upper)

    pmin, pmax = pixel_array.min(), pixel_array.max()
    if pmax - pmin == 0:
        return np.zeros_like(pixel_array, dtype=np.uint8)
    result: np.ndarray = ((pixel_array - pmin) / (pmax - pmin) * 255).astype(np.uint8)
    return result


def convert_dcm_to_jpeg(dcm_path: Path, output_path: Path) -> None:
    """Read a DICOM file and save it as JPEG."""
    ds = pydicom.dcmread(dcm_path)
    pixel_array = ds.pixel_array.astype(np.float64)

    normalized = apply_windowing(pixel_array, ds)

    image = Image.fromarray(normalized)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(output_path, "JPEG", quality=95)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert DICOM files to JPEG.",
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Root directory containing .dcm files",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output directory (default: <directory>/jpeg)",
    )
    args = parser.parse_args()

    root: Path = args.directory.resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_dir = (args.output or root / "jpeg").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    dcm_files = sorted(root.rglob("*.dcm"))
    if not dcm_files:
        print("No .dcm files found.")
        return

    used_names: set[str] = set()
    for dcm_path in dcm_files:
        stem = dcm_path.stem
        out_name = f"{stem}.jpeg"
        if out_name in used_names:
            counter = 1
            while f"{stem}_{counter}.jpeg" in used_names:
                counter += 1
            out_name = f"{stem}_{counter}.jpeg"
        used_names.add(out_name)

        output_path = output_dir / out_name
        try:
            convert_dcm_to_jpeg(dcm_path, output_path)
            print(
                f"  {dcm_path.relative_to(root)} -> {output_path.name}",
            )
        except Exception as e:
            print(
                f"  FAILED {dcm_path.relative_to(root)}: {e}",
                file=sys.stderr,
            )

    print(f"\nDone. {len(dcm_files)} file(s) processed -> {output_dir}")


if __name__ == "__main__":
    main()
