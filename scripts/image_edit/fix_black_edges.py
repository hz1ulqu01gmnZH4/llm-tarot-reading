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
import glob
import os
import shutil

def find_card_boundary(img_array, threshold=50):
    """
    Find the actual card boundary by detecting where black edges end.
    
    Returns: (top, bottom, left, right) boundaries
    """
    height, width = img_array.shape[:2]
    
    # Convert to grayscale for easier edge detection
    gray = np.mean(img_array, axis=2)
    
    # Find top boundary
    top = 0
    for i in range(height // 2):
        row_brightness = np.mean(gray[i, :])
        if row_brightness > threshold:
            top = max(0, i - 2)  # Back up a bit to ensure we get the edge
            break
    
    # Find bottom boundary
    bottom = height
    for i in range(height - 1, height // 2, -1):
        row_brightness = np.mean(gray[i, :])
        if row_brightness > threshold:
            bottom = min(height, i + 3)
            break
    
    # Find left boundary
    left = 0
    for i in range(width // 2):
        col_brightness = np.mean(gray[:, i])
        if col_brightness > threshold:
            left = max(0, i - 2)
            break
    
    # Find right boundary
    right = width
    for i in range(width - 1, width // 2, -1):
        col_brightness = np.mean(gray[:, i])
        if col_brightness > threshold:
            right = min(width, i + 3)
            break
    
    return top, bottom, left, right

def fix_black_edges_transparency(image_path, output_path=None, threshold=50):
    """
    Replace black edges with transparency.
    """
    img = Image.open(image_path).convert('RGBA')
    img_array = np.array(img)
    
    # Create mask for black pixels
    rgb = img_array[:, :, :3]
    
    # Pixels are considered black if all RGB values are below threshold
    black_mask = np.all(rgb <= threshold, axis=2)
    
    # Apply transparency to black pixels (but only on edges, not in the card itself)
    # Find card boundary first
    top, bottom, left, right = find_card_boundary(rgb, threshold)
    
    # Create edge mask (pixels outside the detected card area)
    edge_mask = np.zeros_like(black_mask, dtype=bool)
    edge_mask[:top, :] = True
    edge_mask[bottom:, :] = True
    edge_mask[:, :left] = True
    edge_mask[:, right:] = True
    
    # Only make edge black pixels transparent
    final_mask = black_mask & edge_mask
    img_array[final_mask, 3] = 0  # Set alpha to 0 for black edge pixels
    
    # Save result
    result_img = Image.fromarray(img_array, 'RGBA')
    if output_path:
        result_img.save(output_path)
    else:
        result_img.save(image_path)  # Overwrite original
    
    return True

def fix_black_edges_crop(image_path, output_path=None, threshold=50):
    """
    Crop black edges from the image.
    """
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    
    # Find card boundary
    top, bottom, left, right = find_card_boundary(img_array, threshold)
    
    # Crop image
    cropped = img.crop((left, top, right, bottom))
    
    # Resize back to original dimensions to maintain consistency
    original_size = img.size
    cropped = cropped.resize(original_size, Image.Resampling.LANCZOS)
    
    # Save result
    if output_path:
        cropped.save(output_path)
    else:
        cropped.save(image_path)  # Overwrite original
    
    return True

def process_problematic_images(method='transparency'):
    """
    Process all images with black edges.
    
    Args:
        method: 'transparency' or 'crop'
    """
    # List of problematic images from the detection
    problematic = [
        '00_the_fool.png', '11_justice.png', '15_the_devil.png', '18_the_moon.png',
        'cups_05.png', 'cups_06.png', 'cups_08.png', 'cups_10.png',
        'pentacles_02.png', 'pentacles_04.png', 'pentacles_05.png', 'pentacles_06.png',
        'pentacles_07.png', 'pentacles_08.png', 'pentacles_11_page.png', 'pentacles_14_king.png',
        'swords_04.png', 'swords_07.png', 'swords_11_page.png', 'swords_12_knight.png',
        'wands_02.png', 'wands_03.png', 'wands_07.png', 'wands_10.png',
        'wands_12_knight.png', 'wands_14_king.png'
    ]
    
    # Create backup directory
    backup_dir = 'images/backup_black_edges'
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Processing {len(problematic)} images with {method} method...")
    print("Creating backups in images/backup_black_edges/")
    print("=" * 60)
    
    fixed_count = 0
    for filename in problematic:
        img_path = f'images/{filename}'
        if os.path.exists(img_path):
            # Create backup
            backup_path = f'{backup_dir}/{filename}'
            shutil.copy2(img_path, backup_path)
            
            try:
                if method == 'transparency':
                    success = fix_black_edges_transparency(img_path)
                else:  # crop
                    success = fix_black_edges_crop(img_path)
                
                if success:
                    print(f"✅ Fixed: {filename}")
                    fixed_count += 1
                else:
                    print(f"❌ Failed: {filename}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Fixed {fixed_count}/{len(problematic)} images")
    print(f"Originals backed up in: {backup_dir}")
    
    return fixed_count

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--crop':
        # Use crop method
        process_problematic_images(method='crop')
    elif len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test on a single image
        test_img = 'images/00_the_fool.png'
        if os.path.exists(test_img):
            print(f"Testing transparency fix on {test_img}")
            fix_black_edges_transparency(test_img, 'test_transparent.png')
            print("Saved test result to test_transparent.png")
    else:
        # Default: use transparency method
        process_problematic_images(method='transparency')