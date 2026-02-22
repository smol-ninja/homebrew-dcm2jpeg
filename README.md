# dcm2jpeg

Convert DICOM (`.dcm`) files to JPEG. Recursively finds all DICOM files in a directory and outputs
flat JPEG files — no nested directories.

## Install

### Homebrew

```bash
brew tap smol-ninja/dcm2jpeg
brew install dcm2jpeg
```

### pip

```bash
pip install git+https://github.com/smol-ninja/homebrew-dcm2jpeg.git
```

## Usage

```bash
# Convert all .dcm files in the current directory
dcm2jpeg .

# Convert with a custom output directory
dcm2jpeg /path/to/dicoms --output /path/to/output
```

### Example

Given this structure:

```
scans/
├── file1.dcm
└── series1/
    └── file2.dcm
```

Running `dcm2jpeg scans/` produces:

```
scans/
└── jpeg/
    ├── file1.jpeg
    └── file2.jpeg
```

All output files are placed in a single flat `jpeg/` directory. Duplicate filenames from different
subdirectories are disambiguated with `_1`, `_2`, etc.

## Features

- Recursive `.dcm` file discovery
- DICOM windowing (window center/width) for proper contrast
- Flat output directory (no nested folders)
- Duplicate filename handling
- 95% JPEG quality

## Development

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just).

```bash
# Install dependencies
just install

# Run all checks
just check

# Auto-fix lint issues
just fix
```

## License

[MIT](LICENSE)
