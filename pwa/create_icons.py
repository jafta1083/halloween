#!/usr/bin/env python3
"""Generate PWA icons (192x192 and 512x512) with Halloween pumpkin theme."""

from PIL import Image, ImageDraw
import os

def create_icon(size: int) -> Image.Image:
    """Create a Halloween-themed pumpkin icon."""
    # Dark background
    img = Image.new('RGB', (size, size), color='#0e1117')
    draw = ImageDraw.Draw(img)
    
    center_x = size / 2
    center_y = size / 2
    radius = int(size * 0.45)
    
    # Draw orange circle (pumpkin body)
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill='#ff6b00'
    )
    
    # Eyes
    eye_width = int(size * 0.08)
    eye_height = int(size * 0.08)
    eye_y = int(center_y - size * 0.1)
    
    # Left eye
    draw.rectangle(
        [int(center_x - size * 0.15), eye_y, int(center_x - size * 0.15 + eye_width), int(eye_y + eye_height)],
        fill='#0e1117'
    )
    
    # Right eye
    draw.rectangle(
        [int(center_x + size * 0.07), eye_y, int(center_x + size * 0.07 + eye_width), int(eye_y + eye_height)],
        fill='#0e1117'
    )
    
    # Mouth (triangle)
    mouth_points = [
        (int(center_x - size * 0.1), int(center_y + size * 0.05)),
        (int(center_x + size * 0.1), int(center_y + size * 0.05)),
        (int(center_x), int(center_y + size * 0.15))
    ]
    draw.polygon(mouth_points, fill='#0e1117')
    
    # Stem (green)
    stem_x1 = int(center_x - size * 0.02)
    stem_x2 = int(center_x + size * 0.02)
    stem_y1 = int(center_y - radius)
    stem_y2 = int(center_y - radius + size * 0.1)
    draw.rectangle([stem_x1, stem_y1, stem_x2, stem_y2], fill='#228B22')
    
    return img

def main():
    """Generate and save both icon sizes."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create 192x192 icon
    icon_192 = create_icon(192)
    path_192 = os.path.join(script_dir, 'icon-192.png')
    icon_192.save(path_192, 'PNG')
    print(f"✓ Created {path_192}")
    
    # Create 512x512 icon
    icon_512 = create_icon(512)
    path_512 = os.path.join(script_dir, 'icon-512.png')
    icon_512.save(path_512, 'PNG')
    print(f"✓ Created {path_512}")

if __name__ == '__main__':
    main()
