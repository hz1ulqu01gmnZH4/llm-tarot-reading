#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
#   "numpy",
# ]
# ///

from PIL import Image
import numpy as np
import os
import shutil

def find_content_bounds(img_array, threshold=30, margin=5):
    """
    Find the actual content boundaries by detecting where black/dark edges end.
    Returns: (left, top, right, bottom) boundaries
    """
    height, width = img_array.shape[:2]
    
    # Convert to grayscale for easier edge detection
    if len(img_array.shape) == 3:
        gray = np.mean(img_array[:, :, :3], axis=2)
    else:
        gray = img_array
    
    # Find top boundary - scan from top down
    top = 0
    for y in range(height):
        row_max = np.max(gray[y, :])
        if row_max > threshold:
            top = max(0, y - margin)
            break
    
    # Find bottom boundary - scan from bottom up
    bottom = height
    for y in range(height - 1, -1, -1):
        row_max = np.max(gray[y, :])
        if row_max > threshold:
            bottom = min(height, y + margin + 1)
            break
    
    # Find left boundary - scan from left to right
    left = 0
    for x in range(width):
        col_max = np.max(gray[:, x])
        if col_max > threshold:
            left = max(0, x - margin)
            break
    
    # Find right boundary - scan from right to left
    right = width
    for x in range(width - 1, -1, -1):
        col_max = np.max(gray[:, x])
        if col_max > threshold:
            right = min(width, x + margin + 1)
            break
    
    return left, top, right, bottom

def auto_crop_and_resize(image_path, output_path=None, target_size=(600, 1000), threshold=30):
    """
    Automatically crop black edges and resize to target dimensions.
    
    Args:
        image_path: Path to input image
        output_path: Path to save output (if None, overwrites input)
        target_size: Target dimensions (width, height)
        threshold: Brightness threshold for edge detection
    """
    # Open image
    img = Image.open(image_path)
    original_mode = img.mode
    
    # Convert to RGBA for processing
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    img_array = np.array(img)
    
    # Find content boundaries
    left, top, right, bottom = find_content_bounds(img_array, threshold)
    
    # Crop to content
    cropped = img.crop((left, top, right, bottom))
    
    # Calculate aspect ratios
    cropped_width = right - left
    cropped_height = bottom - top
    cropped_aspect = cropped_width / cropped_height if cropped_height > 0 else 1
    target_aspect = target_size[0] / target_size[1]
    
    # Resize with aspect ratio preservation and padding if needed
    if abs(cropped_aspect - target_aspect) > 0.1:  # Significant aspect ratio difference
        # Resize to fit within target while maintaining aspect ratio
        cropped.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create new image with target size and paste cropped image centered
        new_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
        
        # Calculate position to center the image
        x_offset = (target_size[0] - cropped.width) // 2
        y_offset = (target_size[1] - cropped.height) // 2
        
        new_img.paste(cropped, (x_offset, y_offset))
        result = new_img
    else:
        # Direct resize if aspect ratios are similar
        result = cropped.resize(target_size, Image.Resampling.LANCZOS)
    
    # Save result
    save_path = output_path or image_path
    result.save(save_path)
    
    return {
        'original_size': img.size,
        'crop_bounds': (left, top, right, bottom),
        'cropped_size': (cropped_width, cropped_height),
        'final_size': result.size,
        'saved_to': save_path
    }

def process_all_black_edge_images():
    """Process all images with black edges."""
    
    # List of problematic images
    problematic = [
        '00_the_fool.png', '11_justice.png', '15_the_devil.png', '18_the_moon.png',
        'cups_05.png', 'cups_06.png', 'cups_08.png', 'cups_10.png',
        'pentacles_02.png', 'pentacles_04.png', 'pentacles_05.png', 'pentacles_06.png',
        'pentacles_07.png', 'pentacles_08.png', 'pentacles_11_page.png', 'pentacles_14_king.png',
        'swords_04.png', 'swords_07.png', 'swords_11_page.png', 'swords_12_knight.png',
        'wands_02.png', 'wands_03.png', 'wands_07.png', 'wands_10.png',
        'wands_12_knight.png', 'wands_14_king.png'
    ]
    
    # Create output directory for processed images
    output_dir = 'images/cropped_resized'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Cropping and resizing images with black edges...")
    print(f"Target size: 600x1000")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    
    successful = 0
    failed = []
    
    for filename in problematic:
        # Use backup if available, otherwise use current
        backup_path = f'images/backup_black_edges/{filename}'
        current_path = f'images/{filename}'
        
        if os.path.exists(backup_path):
            input_path = backup_path
            print(f"Processing backup: {filename}")
        elif os.path.exists(current_path):
            input_path = current_path
            print(f"Processing current: {filename}")
        else:
            print(f"❌ Not found: {filename}")
            failed.append(filename)
            continue
        
        output_path = f'{output_dir}/{filename}'
        
        try:
            info = auto_crop_and_resize(input_path, output_path)
            print(f"  ✅ Cropped from {info['crop_bounds']} -> {info['final_size']}")
            successful += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed.append(filename)
    
    print("\n" + "=" * 60)
    print(f"Successfully processed: {successful}/{len(problematic)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    
    # Option to replace originals
    print("\nProcessed images saved in: images/cropped_resized/")
    print("To replace originals, run:")
    print("  cp images/cropped_resized/*.png images/")
    
    return successful, failed

def preview_single_image(image_path):
    """Preview crop bounds for a single image."""
    img = Image.open(image_path)
    img_array = np.array(img)
    
    left, top, right, bottom = find_content_bounds(img_array)
    
    print(f"Image: {image_path}")
    print(f"Original size: {img.size}")
    print(f"Detected content bounds: ({left}, {top}, {right}, {bottom})")
    print(f"Content size: {right-left}x{bottom-top}")
    print(f"Will crop {left} pixels from left, {top} from top")
    print(f"Will crop {img.width-right} pixels from right, {img.height-bottom} from bottom")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--preview':
            # Preview mode for single image
            if len(sys.argv) > 2:
                preview_single_image(sys.argv[2])
            else:
                print("Usage: python crop_and_resize.py --preview <image_path>")
        else:
            # Process single image
            input_path = sys.argv[1]
            output_path = sys.argv[2] if len(sys.argv) > 2 else None
            info = auto_crop_and_resize(input_path, output_path)
            print(f"Processed: {input_path}")
            print(f"  Original: {info['original_size']}")
            print(f"  Cropped: {info['cropped_size']}")
            print(f"  Final: {info['final_size']}")
            print(f"  Saved to: {info['saved_to']}")
    else:
        # Process all problematic images
        process_all_black_edge_images()