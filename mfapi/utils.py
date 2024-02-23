import requests
import os
from PIL import Image
from io import BytesIO

def get_tetras_url(url):
    prefix = "https://files.tetras-libre.fr/"
    split = url.split("https://filebrowser.tetras-libre.fr/files/www/")[1]
    return os.path.join(prefix, split)

def get_online_image_dims(url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    width, height = img.size
    return width, height