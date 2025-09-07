#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
# ]
# ///

from PIL import Image
import sys

img_path = sys.argv[1] if len(sys.argv) > 1 else 'generated_images/images_04_the_emperor_test_2025-09-05T15-47-10-301Z_1.png'
img = Image.open(img_path)
print(f'Size: {img.size}')
print(f'Width: {img.width}px, Height: {img.height}px')
print(f'Aspect ratio: {img.width/img.height:.3f} (Target: 0.667 for 2:3)')