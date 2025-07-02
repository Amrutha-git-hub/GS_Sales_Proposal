import requests
from io import BytesIO
from colorthief import ColorThief


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_color_from_image(image_url):
    response = requests.get(image_url)
    img_file = BytesIO(response.content)
    color_thief = ColorThief(img_file)
    palette = color_thief.get_palette(color_count=6)
    hex_colors = [rgb_to_hex(color) for color in palette]
    return hex_colors



def clean_to_list(result:str) :
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```json'):
        result = result[len('```json'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    return result

