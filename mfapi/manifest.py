import iiif_prezi3
import os
import uuid
import pprint
import json
import requests
from .utils import online_img_to_np, get_temp_file
from.mediabody import MediaBody

def read_manifest(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        new_manifest = Manifest()
        
        new_manifest.manifest = iiif_prezi3.Manifest(**json_data)
        return new_manifest

class Manifest():
    def __init__(self, **kwargs) -> None:
        self.__dict__["id_prefix"] = kwargs.get("id_prefix", "https://files.tetras-libre.fr/")
        self.__dict__["manifest_path"] = kwargs.get("manifest_path", "manifests")
        self.__dict__["uuid"] = str(uuid.uuid4())

        self.__dict__["logo"] = MediaBody(id = kwargs.get("logo", "https://univ-droit.fr/images/structures/universites/356/0350937d.jpg"))

        self.__dict__["manifest"] = iiif_prezi3.Manifest(
            id = os.path.join(self.id_prefix, self.manifest_path, f"{self.uuid}.json"),
            label = kwargs.get("label", {"en" : ["Untitled Manifest"]}),
            rights = kwargs.get("rights", "https://creativecommons.org/licenses/by-nc-nd/4.0/")
        )

    def to_dict(self) -> dict:
        manifest_dict = self.manifest.dict()
        manifest_dict["logo"] = self.logo.to_dict()
        manifest_dict["@context"] = "http://iiif.io/api/presentation/3/context.json"
        return manifest_dict
    
    def get_media(self, canvas = 0):
        return self.manifest.items[canvas].items[0].items[0].body
    
    def media_to_np(self, canvas = 0):
        media_info = self.get_media(canvas)
        if media_info.type == "Image":
            return online_img_to_np(media_info.id)

    def print(self):
        pprint.pprint(self.to_dict())

    def to_json(self):
        json_data = self.to_dict()
        temp_path = get_temp_file("json", self.uuid)
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii = False, indent = 2)
        return temp_path

    def add_metadata(self, label, value):
        if self.manifest.metadata != None:
            self.manifest.metadata.append({"label" : label, "value" : value})
        else:
            self.manifest.metadata = [{"label" : label, "value" : value}]

    def add_canvas_from_media(self, media_url, **kwargs):
        num_canvases = len(self.manifest.items)
        canvas_path = os.path.join(self.id_prefix, self.manifest_path, "canvas", str(num_canvases + 1))
        
        media_body = MediaBody(id = media_url)

        canvas = iiif_prezi3.Canvas(
            id = canvas_path,
            label = kwargs.get("label", {"en" : [os.path.basename(media_url)]})
        )

        if media_body.type == "Image" or media_body.type == "Video":
            canvas.width = media_body.width
            canvas.height = media_body.height
        if media_body.type == "Audio" or media_body.type == "Video":
            canvas.duration = media_body.duration

        ap = iiif_prezi3.AnnotationPage(id = os.path.join(canvas_path, "page", "1"))
        
        if media_body.type == "Image":
            annotation_target = canvas_path + f"#xywh=0,0,{media_body.width},{media_body.height}"
        elif media_body.type == "Video":
            annotation_target = canvas_path + f"#xywh=0,0,{media_body.width},{media_body.height}&t=0,{media_body.duration}"
        elif media_body.type == "Audio":
            annotation_target = canvas_path + f"#t=0,{media_body.duration}"

        an = iiif_prezi3.Annotation(
            id = os.path.join(canvas_path, "page", "1", "1"),
            target = annotation_target,
            motivation = "painting",
            body = media_body.to_dict()
        )

        ap.items.append(an)
        canvas.items.append(ap)
        self.manifest.items.append(canvas)

    def __getattr__(self, attr):
        if attr in self.manifest.__dict__ and attr not in self.__dict__:
            return getattr(self.manifest, attr)
        else:
            return self.__getattr__(attr)
        
    def __setattr__(self, attr, value) -> None:
        if attr in self.manifest.__dict__ and attr not in self.__dict__:
            setattr(self.manifest, attr, value)
        else:
            super().__setattr__(attr, value)