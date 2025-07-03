from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, filename="text_image.png"):
    """
    Create a clean, professional image with black text on white background
    """
    
    # Try to get a professional font
    try:
        # Try professional fonts first
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 32)  # Windows
        except:
            try:
                font = ImageFont.truetype("Helvetica.ttc", 32)  # Mac
            except:
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)  # Linux
                except:
                    font = ImageFont.load_default()
    
    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1), 'white')
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Get text dimensions
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Create final image with some padding
    padding = 50
    img_width = text_width + (padding * 2)
    img_height = text_height + (padding * 2)
    
    # Create clean white background
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw text in strong black, centered
    x = padding
    y = padding
    draw.text((x, y), text, font=font, fill='black')
    
    # Save image
    img.save(filename, 'PNG', quality=100)
    print(f"✓ Image saved: {filename}")
    return filename
