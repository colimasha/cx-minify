#!/usr/bin/env python3
"""
cx-minify - Simple lossless compression tool for AI models
Compress and decompress files without quality loss
"""

import lzma
import os
import sys
import argparse
from pathlib import Path


def get_file_size(filepath):
    """Get file size in human-readable format"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def compress_file(input_path, output_path=None, level=9):
    """
    Compress a file using LZMA compression
    level: 0-9, where 9 is maximum compression (default)
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: File '{input_path}' not found")
        return False

    if output_path is None:
        output_path = Path(str(input_path) + '.cxm')
    else:
        output_path = Path(output_path)

    print(f"Compressing: {input_path}")
    print(f"Original size: {get_file_size(input_path)}")

    try:
        with open(input_path, 'rb') as f_in:
            with lzma.open(output_path, 'wb', preset=level) as f_out:
                chunk_size = 1024 * 1024  # 1MB chunks
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)

        print(f"Compressed size: {get_file_size(output_path)}")
        ratio = (1 - os.path.getsize(output_path) / os.path.getsize(input_path)) * 100
        print(f"Space saved: {ratio:.1f}%")
        print(f"Output: {output_path}")
        return True

    except Exception as e:
        print(f"Error during compression: {e}")
        return False


def decompress_file(input_path, output_path=None):
    """
    Decompress a .cxm file
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: File '{input_path}' not found")
        return False

    if output_path is None:
        if input_path.suffix == '.cxm':
            output_path = input_path.with_suffix('')
        else:
            output_path = Path(str(input_path) + '.decompressed')
    else:
        output_path = Path(output_path)

    print(f"Decompressing: {input_path}")
    print(f"Compressed size: {get_file_size(input_path)}")

    try:
        with lzma.open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                chunk_size = 1024 * 1024  # 1MB chunks
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    f_out.write(chunk)

        print(f"Decompressed size: {get_file_size(output_path)}")
        print(f"Output: {output_path}")
        return True

    except Exception as e:
        print(f"Error during decompression: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='cx-minify - Lossless compression for AI models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Compress a model:
    python cx-minify.py compress model.bin
    python cx-minify.py compress model.bin -o model.cxm

  Decompress a model:
    python cx-minify.py decompress model.cxm
    python cx-minify.py decompress model.cxm -o model.bin
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Compress a file')
    compress_parser.add_argument('input', help='Input file to compress')
    compress_parser.add_argument('-o', '--output', help='Output file (default: input.cxm)')
    compress_parser.add_argument('-l', '--level', type=int, default=9, choices=range(0, 10),
                                help='Compression level 0-9 (default: 9, max compression)')

    # Decompress command
    decompress_parser = subparsers.add_parser('decompress', help='Decompress a file')
    decompress_parser.add_argument('input', help='Input file to decompress')
    decompress_parser.add_argument('-o', '--output', help='Output file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'compress':
        success = compress_file(args.input, args.output, args.level)
    elif args.command == 'decompress':
        success = decompress_file(args.input, args.output)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
