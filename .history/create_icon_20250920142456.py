#!/usr/bin/env python
"""
Create a professional icon for the GUI application
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        """Create a professional security scanner icon."""
        # Create a 64x64 image with transparent background
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw shield background
        shield_color = (52, 152, 219)  # Blue
        draw.ellipse([8, 8, 56, 56], fill=shield_color)
        
        # Draw inner shield
        inner_color = (255, 255, 255)  # White
        draw.ellipse([12, 12, 52, 52], fill=inner_color)
        
        # Draw security symbol (lock)
        lock_color = (52, 152, 219)  # Blue
        # Lock body
        draw.rectangle([24, 32, 40, 44], fill=lock_color)
        # Lock shackle
        draw.arc([26, 20, 38, 32], 0, 180, fill=lock_color, width=3)
        
        # Draw scan lines
        scan_color = (46, 204, 113)  # Green
        for i in range(3):
            y = 20 + i * 8
            draw.line([16, y, 48, y], fill=scan_color, width=2)
        
        # Save as ICO file
        img.save('icon.ico', format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
        print("Icon created successfully!")
        
    if __name__ == "__main__":
        create_icon()
        
except ImportError:
    print("PIL not available, skipping icon creation")
    print("Install with: pip install Pillow")
