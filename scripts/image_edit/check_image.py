#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
# ]
# ///

from PIL import Image
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else 'images/00_the_fool.png'
img = Image.open(img_path)
print(f'Image: {img_path}')
print(f'Mode: {img.mode}')
print(f'Size: {img.size}')
print(f'Has alpha: {img.mode == "RGBA"}')