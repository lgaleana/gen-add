from PIL import Image
import requests
from io import BytesIO

def get_image_dimensions(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img.size