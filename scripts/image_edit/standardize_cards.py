#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
#   "numpy",
# ]
# ///

from PIL import Image
import glob
import os

def analyze_and_standardize():
    # Target dimensions for tarot cards (3:5 ratio is traditional)
    TARGET_WIDTH = 600
    TARGET_HEIGHT = 1000
    
    # Check all existing images
    image_files = glob.glob("images/*.png") + glob.glob("generated_images/*.png")
    
    print("Current image dimensions:")
    for img_path in image_files:
        if "transparent" in img_path:
            continue
        img = Image.open(img_path)
        print(f"{os.path.basename(img_path)}: {img.size}")
    
    print(f"\nTarget dimensions: {TARGET_WIDTH}x{TARGET_HEIGHT}")
    print("\nNote: When generating new cards, we should specify consistent dimensions.")
    print("The API uses 1024x1536 which maintains roughly the same 2:3 aspect ratio.")
    
    # Optional: resize existing images
    response = input("\nDo you want to resize existing images to standard size? (y/n): ")
    if response.lower() == 'y':
        for img_path in image_files:
            if "transparent" in img_path:
                continue
            img = Image.open(img_path)
            if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
                # Resize maintaining aspect ratio and crop/pad as needed
                img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
                
                # Create new image with target size and paste centered
                new_img = Image.new('RGBA', (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
                x = (TARGET_WIDTH - img.width) // 2
                y = (TARGET_HEIGHT - img.height) // 2
                new_img.paste(img, (x, y))
                
                # Save with _standard suffix
                output_path = img_path.replace('.png', '_standard.png')
                new_img.save(output_path)
                print(f"Standardized: {os.path.basename(output_path)}")

if __name__ == "__main__":
    analyze_and_standardize()