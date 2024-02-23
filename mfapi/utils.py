import requests
from PIL import Image
from io import BytesIO

def get_online_image_dims(url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    img = Image.open(img_data)
    width, height = img.size
    return width, height