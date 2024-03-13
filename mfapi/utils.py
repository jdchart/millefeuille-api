import requests
import os
from PIL import Image
from io import BytesIO
import cv2
from pydub import AudioSegment
import uuid
import shutil

def get_temp_file(file_ext, file_name = None, folder_name = "temp"):
    if file_name == None:
        file_name = str(uuid.uuid4())
    full_path = os.path.join(os.getcwd(), folder_name, f"{file_name}.{file_ext}")
    if os.path.isdir(os.path.dirname(full_path)) == False:
        os.makedirs(os.path.dirname(full_path))
    return full_path

def clean_up(folder_name = "temp"):
    if os.path.isdir(os.path.join(os.getcwd(), folder_name)):
        shutil.rmtree(os.path.join(os.getcwd(), folder_name))

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

def dl_all(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 206 or response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

def dl_range(url, range, path):
    response = requests.get(url, headers={'Range': f'bytes={range}'}, stream=True)
    if response.status_code == 206:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

def get_online_video_dims(url):
    dl_path = get_temp_file("mp4", None, "temp_media")
    
    try:
        dl_range(url, "0-5242880", dl_path)
        vid = cv2.VideoCapture(dl_path)
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width < 1 or height < 1:
            raise Exception("Width or height was smaller than 1.")

        clean_up("temp_media")
        return width, height
    except:
        print("Unable to retrive video data from beginning of file, downloading whole file...")
        dl_all(url, dl_path)
        vid = cv2.VideoCapture(dl_path)
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # print(f"WIDTH: {width}" )
        # print(f"HEIGHT: {height}" )

        clean_up("temp_media")
        return width, height

def get_online_video_duration(url):
    # TODO make it try different download ranges until it is successful
    dl_path = get_temp_file("mp4", None, "temp_media")

    # #dl_range(url, "0-5242880", dl_path)
    # dl_all(url, dl_path)
    # vid = cv2.VideoCapture(dl_path)
    
    # num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(f"NUMM FRAMES: {num_frames}")
    # fps = vid.get(cv2.CAP_PROP_FPS)
    # print(f"FPS: {fps}")
    # duration = num_frames / fps

    # clean_up("temp_media")
    # return duration
    
    try:
        dl_range(url, "0-5242880", dl_path)
        vid = cv2.VideoCapture(dl_path)
        
        num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = vid.get(cv2.CAP_PROP_FPS)
        duration = num_frames / fps

        clean_up("temp_media")
        return duration
    except:
        print("Unable to retrive video data from beginning of file, downloading whole file...")
        dl_all(url, dl_path)
        vid = cv2.VideoCapture(dl_path)
        
        num_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = vid.get(cv2.CAP_PROP_FPS)
        duration = num_frames / fps

        clean_up("temp_media")
        return duration


def get_online_audio_duration(url):
    dl_path = get_temp_file("mp3", None, "temp_media")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dl_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        audio = AudioSegment.from_file(dl_path)
        duration = len(audio) / 1000.0 
        clean_up("temp_media")
        return duration
    
def online_img_to_np(url):
    dl_path = get_temp_file("jpg", None, "temp_media")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dl_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        
        # Taken from dvt (so that it'll work with dvt...):
        img = cv2.imread(_expand_path(dl_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        clean_up("temp_media")
        return img

def _expand_path(path: str) -> str:
    path = os.path.abspath(os.path.expanduser(path))
    return path