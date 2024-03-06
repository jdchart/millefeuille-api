import requests
import os
from PIL import Image
from io import BytesIO
import cv2
from pydub import AudioSegment

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


def dl_range(url, range, path):
    response = requests.get(url, headers={'Range': f'bytes={range}'}, stream=True)
    if response.status_code == 206:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

def get_online_video_dims(url):
    dl_path = os.path.join(os.getcwd(), "temp.mp4")
    dl_range(url, "0-5242880", dl_path)
    vid = cv2.VideoCapture(dl_path)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    os.remove(dl_path)
    return width, height

def get_online_video_duration(url):
    dl_path = os.path.join(os.getcwd(), "temp.mp4")
    dl_range(url, "0-5242880", dl_path)
    vid = cv2.VideoCapture(dl_path)
    
    num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vid.get(cv2.CAP_PROP_FPS)
    duration = num_frames / fps

    os.remove(dl_path)
    return duration

def get_online_audio_duration(url):
    dl_path = os.path.join(os.getcwd(), "temp.mp3")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dl_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        audio = AudioSegment.from_file(dl_path)
        duration = len(audio) / 1000.0 
        os.remove(dl_path)
        return duration
    


def online_img_to_np(url):
    dl_path = os.path.join(os.getcwd(), "temp.jpg")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dl_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        # Taken from dvt (so that itll work with dvt...):
        img = cv2.imread(_expand_path(dl_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        os.remove(dl_path)


        return img


def _expand_path(path: str) -> str:
    path = os.path.abspath(os.path.expanduser(path))
    return path
    

# def get_online_duration(url):
#     response = requests.head(url)
#     if response.status_code == 200:
#         # Get the content length and content range from the headers
#         content_length = response.headers.get('Content-Length')
#         content_range = response.headers.get('Content-Range')

#         # Parse the content range to get the file size
#         if content_range:
#             file_size = int(content_range.split('/')[-1])
#         elif content_length:
#             file_size = int(content_length)
#         else:
#             raise Exception("Unable to determine file size.")

#         # Calculate duration based on assumptions about the file format
#         # Adjust this based on the actual file format you are working with
#         assumed_bitrate = 128  # Adjust this based on your assumptions about the bitrate
#         duration = file_size / (assumed_bitrate * 1024 / 8)  # in seconds

#         return duration