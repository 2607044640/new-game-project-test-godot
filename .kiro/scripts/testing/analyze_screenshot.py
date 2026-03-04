#!/usr/bin/env python3
"""Analyze screenshot for icons"""

from PIL import Image
import sys

def analyze_screenshot(image_path):
    """Analyze screenshot and count visible elements"""
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"Screenshot size: {width}x{height}")
        print(f"Mode: {img.mode}")
        
        # Get pixel data
        pixels = img.load()
        
        # Sample some pixels to understand the image
        print("\nSample pixels (top-left corner):")
        for y in range(min(5, height)):
            row = []
            for x in range(min(10, width)):
                pixel = pixels[x, y]
                if isinstance(pixel, tuple):
                    row.append(f"({pixel[0]},{pixel[1]},{pixel[2]})")
                else:
                    row.append(str(pixel))
            print(f"Row {y}: {' '.join(row[:5])}")
        
        # Check if image is mostly one color (empty scene)
        # Sample center area
        center_x, center_y = width // 2, height // 2
        sample_size = 50
        colors = set()
        
        for y in range(max(0, center_y - sample_size), min(height, center_y + sample_size)):
            for x in range(max(0, center_x - sample_size), min(width, center_x + sample_size)):
                colors.add(pixels[x, y][:3] if isinstance(pixels[x, y], tuple) else pixels[x, y])
        
        print(f"\nUnique colors in center area: {len(colors)}")
        
        # Try to detect icons by looking for distinct colored regions
        # This is a simple heuristic - count non-background colored pixels
        background_color = pixels[0, 0][:3] if isinstance(pixels[0, 0], tuple) else pixels[0, 0]
        print(f"Background color (top-left): {background_color}")
        
        # Count distinct colored regions (very simple approach)
        non_bg_pixels = 0
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y][:3] if isinstance(pixels[x, y], tuple) else pixels[x, y]
                if pixel != background_color:
                    non_bg_pixels += 1
        
        print(f"\nNon-background pixels: {non_bg_pixels} ({non_bg_pixels*100/(width*height):.1f}%)")
        
        # Visual description
        if non_bg_pixels < 100:
            print("\n📊 Analysis: Scene appears mostly empty (likely default Godot scene)")
            print("   No visible game icons detected")
            return 0
        else:
            print("\n📊 Analysis: Scene contains visual elements")
            # Rough estimate based on pixel density
            estimated_icons = max(1, non_bg_pixels // 10000)
            print(f"   Estimated number of distinct elements: ~{estimated_icons}")
            return estimated_icons
            
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return -1

if __name__ == "__main__":
    image_path = ".kiro/TempFolder/current_screenshot.png"
    count = analyze_screenshot(image_path)
    
    print("\n" + "="*60)
    print(f"Icon count: {count}")
    print("="*60)
