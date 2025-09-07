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

def detect_black_edges(image_path, threshold=50, edge_width=10, black_pixel_ratio=0.3):
    """
    Detect if an image has black edges.
    
    Args:
        image_path: Path to the image file
        threshold: RGB values below this are considered "black" (0-255)
        edge_width: How many pixels from the edge to check
        black_pixel_ratio: If more than this ratio of edge pixels are black, flag the image
    
    Returns:
        tuple: (has_black_edges, black_pixel_percentage, edge_stats)
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # Extract edge pixels
        edges = []
        
        # Top edge
        edges.append(img_array[:edge_width, :])
        # Bottom edge
        edges.append(img_array[-edge_width:, :])
        # Left edge
        edges.append(img_array[:, :edge_width])
        # Right edge
        edges.append(img_array[:, -edge_width:])
        
        # Combine all edges
        all_edge_pixels = []
        for edge in edges:
            all_edge_pixels.extend(edge.reshape(-1, 3))
        
        all_edge_pixels = np.array(all_edge_pixels)
        
        # Calculate how many pixels are "black" (below threshold)
        # Check if all RGB values are below threshold
        black_pixels = np.all(all_edge_pixels <= threshold, axis=1)
        black_count = np.sum(black_pixels)
        total_pixels = len(all_edge_pixels)
        black_percentage = (black_count / total_pixels) * 100
        
        # Get average color of edges
        avg_color = np.mean(all_edge_pixels, axis=0)
        
        # Determine if edges are problematic
        has_black_edges = black_percentage > (black_pixel_ratio * 100)
        
        edge_stats = {
            'avg_rgb': avg_color.tolist(),
            'avg_brightness': np.mean(avg_color),
            'black_pixel_count': int(black_count),
            'total_edge_pixels': total_pixels,
            'corners': check_corners(img_array, threshold)
        }
        
        return has_black_edges, black_percentage, edge_stats
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False, 0, {}

def check_corners(img_array, threshold, corner_size=20):
    """Check the four corners of the image for black pixels."""
    height, width = img_array.shape[:2]
    corners = {
        'top_left': img_array[:corner_size, :corner_size],
        'top_right': img_array[:corner_size, -corner_size:],
        'bottom_left': img_array[-corner_size:, :corner_size],
        'bottom_right': img_array[-corner_size:, -corner_size:]
    }
    
    corner_stats = {}
    for name, corner in corners.items():
        corner_pixels = corner.reshape(-1, 3)
        black_pixels = np.all(corner_pixels <= threshold, axis=1)
        corner_stats[name] = {
            'black_ratio': np.sum(black_pixels) / len(corner_pixels),
            'avg_brightness': np.mean(corner_pixels)
        }
    
    return corner_stats

def analyze_all_cards():
    """Analyze all tarot cards for black edges."""
    image_files = sorted(glob.glob("images/*.png"))
    
    print(f"Analyzing {len(image_files)} images for black edges...")
    print("=" * 80)
    
    problematic_images = []
    borderline_images = []
    clean_images = []
    
    for img_path in image_files:
        filename = os.path.basename(img_path)
        has_black_edges, black_percentage, edge_stats = detect_black_edges(img_path)
        
        if has_black_edges:
            problematic_images.append((filename, black_percentage, edge_stats))
            print(f"❌ {filename}: {black_percentage:.1f}% black pixels (avg brightness: {edge_stats['avg_brightness']:.1f})")
        elif black_percentage > 15:  # Borderline cases
            borderline_images.append((filename, black_percentage, edge_stats))
            print(f"⚠️  {filename}: {black_percentage:.1f}% black pixels (borderline)")
        else:
            clean_images.append(filename)
            # print(f"✅ {filename}: Clean edges")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Clean images: {len(clean_images)}")
    print(f"⚠️  Borderline images: {len(borderline_images)}")
    print(f"❌ Problematic images: {len(problematic_images)}")
    
    if problematic_images:
        print("\nImages that need fixing (black edges detected):")
        for filename, percentage, stats in problematic_images:
            print(f"  - {filename} ({percentage:.1f}% black)")
            # Check which edges are worst
            corners = stats.get('corners', {})
            worst_corners = [name for name, data in corners.items() if data['black_ratio'] > 0.5]
            if worst_corners:
                print(f"    Worst areas: {', '.join(worst_corners)}")
    
    if borderline_images:
        print("\nBorderline images (may need attention):")
        for filename, percentage, stats in borderline_images:
            print(f"  - {filename} ({percentage:.1f}% black)")
    
    return problematic_images, borderline_images, clean_images

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Analyze specific image
        img_path = sys.argv[1]
        has_black_edges, black_percentage, edge_stats = detect_black_edges(img_path)
        print(f"Image: {img_path}")
        print(f"Has black edges: {has_black_edges}")
        print(f"Black pixel percentage: {black_percentage:.2f}%")
        print(f"Average edge brightness: {edge_stats['avg_brightness']:.2f}")
        print(f"Average edge RGB: {edge_stats['avg_rgb']}")
    else:
        # Analyze all images
        analyze_all_cards()