#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
#   "numpy",
# ]
# ///

import sys
import os
from PIL import Image
import numpy as np

def remove_green_background(input_path, output_path, color_threshold=100):
    """
    Remove green chroma key background from image
    color_threshold: tolerance for green color detection
    """
    
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # Create mask for green pixels
    # Green channel should be high, red and blue should be low
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Detect green chroma key (high green, low red and blue)
    green_mask = (g > 150) & (r < 100) & (b < 100)
    
    # Set alpha to 0 for green pixels
    data[green_mask] = [0, 0, 0, 0]
    
    # Create new image
    new_img = Image.fromarray(data, 'RGBA')
    new_img.save(output_path)
    print(f"Processed: {input_path} -> {output_path}")

if __name__ == "__main__":
    import glob
    
    # Process all chroma images
    chroma_files = glob.glob("generated_images/*_chroma_*.png")
    chroma_files.extend(glob.glob("images/*_chroma*.png"))
    
    for input_file in chroma_files:
        # Create output filename
        output_file = input_file.replace("_chroma", "_transparent")
        output_file = output_file.replace("generated_images/", "images/")
        
        remove_green_background(input_file, output_file)
    
    print(f"Processed {len(chroma_files)} files")