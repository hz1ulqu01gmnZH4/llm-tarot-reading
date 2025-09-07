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

def detect_light_edges(image_path, threshold=200, edge_width=10):
    """
    Detect if an image has white/light edges.
    
    Args:
        image_path: Path to the image file
        threshold: RGB values above this are considered "white/light" (0-255)
        edge_width: How many pixels from the edge to check
    """
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    height, width = img_array.shape[:2]
    
    # Extract edge pixels
    edges = []
    edges.append(img_array[:edge_width, :])  # Top
    edges.append(img_array[-edge_width:, :])  # Bottom
    edges.append(img_array[:, :edge_width])  # Left
    edges.append(img_array[:, -edge_width:])  # Right
    
    # Check for light pixels
    light_count = 0
    total_count = 0
    
    for edge in edges:
        edge_pixels = edge.reshape(-1, 3)
        # Check if pixels are light (high RGB values)
        light_pixels = np.mean(edge_pixels, axis=1) > threshold
        light_count += np.sum(light_pixels)
        total_count += len(edge_pixels)
    
    light_percentage = (light_count / total_count) * 100
    return light_percentage > 30  # If more than 30% of edge pixels are light

def find_content_bounds_adaptive(img_array, dark_threshold=30, light_threshold=200, margin=5):
    """
    Find content boundaries by detecting both dark AND light edges.
    """
    height, width = img_array.shape[:2]
    
    if len(img_array.shape) == 3:
        gray = np.mean(img_array[:, :, :3], axis=2)
    else:
        gray = img_array
    
    # Find top boundary - look for content (not too dark, not too light)
    top = 0
    for y in range(height):
        row = gray[y, :]
        # Check if row has actual content (not uniform edge)
        row_std = np.std(row)
        row_mean = np.mean(row)
        if row_std > 10 and dark_threshold < row_mean < light_threshold:
            top = max(0, y - margin)
            break
    
    # Find bottom boundary
    bottom = height
    for y in range(height - 1, -1, -1):
        row = gray[y, :]
        row_std = np.std(row)
        row_mean = np.mean(row)
        if row_std > 10 and dark_threshold < row_mean < light_threshold:
            bottom = min(height, y + margin + 1)
            break
    
    # Find left boundary
    left = 0
    for x in range(width):
        col = gray[:, x]
        col_std = np.std(col)
        col_mean = np.mean(col)
        if col_std > 10 and dark_threshold < col_mean < light_threshold:
            left = max(0, x - margin)
            break
    
    # Find right boundary
    right = width
    for x in range(width - 1, -1, -1):
        col = gray[:, x]
        col_std = np.std(col)
        col_mean = np.mean(col)
        if col_std > 10 and dark_threshold < col_mean < light_threshold:
            right = min(width, x + margin + 1)
            break
    
    return left, top, right, bottom

def fix_edge_and_resize(image_path, output_path=None, target_size=(600, 1000)):
    """
    Remove white/black edges and resize to target dimensions.
    """
    img = Image.open(image_path)
    
    # Convert to RGBA for processing
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    img_array = np.array(img)
    
    # Find content boundaries (handles both black and white edges)
    left, top, right, bottom = find_content_bounds_adaptive(img_array)
    
    print(f"  Detected bounds: ({left}, {top}, {right}, {bottom})")
    print(f"  Cropping: {left}px left, {top}px top, {img.width-right}px right, {img.height-bottom}px bottom")
    
    # Crop to content
    cropped = img.crop((left, top, right, bottom))
    
    # Resize to target size
    result = cropped.resize(target_size, Image.Resampling.LANCZOS)
    
    # Save
    save_path = output_path or image_path
    result.save(save_path)
    
    return save_path

def process_specific_cards():
    """Process cards with white edge issues."""
    
    cards_to_fix = [
        '20_judgement.png',
        # Add any other cards with white edges here
    ]
    
    # First check all cards for light edges
    print("Checking all cards for white/light edges...")
    import glob
    all_cards = glob.glob("images/*.png")
    
    for card_path in all_cards:
        if "backup" in card_path or "test" in card_path:
            continue
        filename = os.path.basename(card_path)
        has_light = detect_light_edges(card_path)
        if has_light:
            print(f"  Found light edges: {filename}")
            if filename not in cards_to_fix:
                cards_to_fix.append(filename)
    
    print(f"\nProcessing {len(cards_to_fix)} cards with edge issues...")
    print("=" * 60)
    
    # Create backup
    os.makedirs("images/backup_white_edges", exist_ok=True)
    
    for filename in cards_to_fix:
        card_path = f"images/{filename}"
        if not os.path.exists(card_path):
            print(f"❌ Not found: {filename}")
            continue
            
        print(f"Processing: {filename}")
        
        # Backup original
        backup_path = f"images/backup_white_edges/{filename}"
        if not os.path.exists(backup_path):
            import shutil
            shutil.copy2(card_path, backup_path)
        
        try:
            fix_edge_and_resize(card_path)
            print(f"  ✅ Fixed and resized to 600x1000\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process single image
        img_path = sys.argv[1]
        print(f"Processing: {img_path}")
        fix_edge_and_resize(img_path)
        print("Done!")
    else:
        # Process all cards with white edges
        process_specific_cards()