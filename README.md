# cx-minify

Simple lossless compression tool for AI models. Compress your AI model files without losing any quality.

## Features

- **Lossless compression** - No quality loss, perfect reconstruction
- **High compression ratio** - Uses LZMA algorithm (typically 20-50% space savings)
- **Simple to use** - Just two commands: compress and decompress
- **No dependencies** - Uses Python standard library only

## Usage

### Compress a file

```bash
python cx-minify.py compress model.bin
```

This creates `model.bin.cxm` (compressed file)

### Compress with custom output name

```bash
python cx-minify.py compress model.bin -o compressed_model.cxm
```

### Decompress a file

```bash
python cx-minify.py decompress model.bin.cxm
```

This restores the original `model.bin`

### Decompress with custom output name

```bash
python cx-minify.py decompress model.cxm -o restored_model.bin
```

### Adjust compression level

```bash
python cx-minify.py compress model.bin -l 6
```

Levels: 0-9 (0=fastest, 9=maximum compression, default=9)

## Example

```bash
# Compress an AI model
python cx-minify.py compress llama-model.bin

# Output:
# Compressing: llama-model.bin
# Original size: 4.21 GB
# Compressed size: 2.87 GB
# Space saved: 31.8%
# Output: llama-model.bin.cxm

# Later, decompress it back
python cx-minify.py decompress llama-model.bin.cxm

# You get the original llama-model.bin back, exactly the same!
```

## Tips

- Keep the original files until you've verified the compressed version works
- The `.cxm` extension stands for "cx-minify"
- Compression is slower than decompression
- Larger files may take several minutes to compress
- Already-compressed formats (zip, tar.gz) won't compress much further

## Requirements

- Python 3.6 or higher
- No external dependencies needed
