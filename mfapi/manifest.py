import iiif_prezi3
import os
import uuid
from .data import media_types
from .utils import get_online_image_dims

class Manifest():
    def __init__(self, **kwargs) -> None:
        self.id_prefix = kwargs.get("id_prefix", "https://files.tetras-libre.fr/")
        self.manifest_path = kwargs.get("manifest_path", "manifests")
        self.uuid = str(uuid.uuid4())

        #self.logo = 

        self.manifest = iiif_prezi3.Manifest(
            id = os.path.join(self.id_prefix, self.manifest_path, f"{self.uuid}.json"),
            label = kwargs.get("label", {"en" : ["Untitled Manifest"]}),
            rights = kwargs.get("rights", "https://creativecommons.org/licenses/by-nc-nd/4.0/")
        )

    def __getattr__(self, attr):
        if attr in self.manifest.__dict__ and attr not in self.__dict__:
            return getattr(self.manifest, attr)
        else:
            return self.__getattr__(attr)
        
    # def __setattr__(self, attr, value) -> None:
    #     if attr in self.manifest.__dict__ and attr not in self.__dict__:
    #         setattr(self.manifest, attr, value)
    #     else:
    #         super().__setattr__(self, attr, value)
        
class MediaBody():
    def __init__(self, **kwargs) -> None:
        self.__dict__["id"] = kwargs.get("id", None)
        self.storage = self.parse_storage()
        self.type = self.parse_type()
        self.format = self.parse_format()
        self.height, self.width = self.parse_dimensions()
        self.duration = self.parse_duration()

    def to_dict(self):
        ret = {}
        for attr in self.__dict__:
            if attr != "storage":
                if getattr(self, attr) != None:
                    ret[attr] = getattr(self, attr)
        return ret

    def parse_storage(self):
        if self.id != None:
            if self.id[:4] == "http":
                return "online"
            else:
                return "local"
        else:
            return None

    def parse_type(self):
        if self.id != None:
            ext = os.path.splitext(self.id)[1][1:]
            for key in media_types:
                if ext in media_types[key]:
                    return key.capitalize()
        else:
            return None

    def parse_format(self):
        if self.id != None:
            ext = os.path.splitext(self.id)[1][1:]
            return f"{self.type.lower()}/{ext}"
        else:
            return None
        
    def parse_dimensions(self):
        if self.type == "Image" or self.type == "Video":
            if self.storage == "online":
                if self.type == "Image":
                    return get_online_image_dims(self.id)
                elif self.type == "Video":
                    return None
            elif self.storage == "local":
                if self.type == "Image":
                    return None
                elif self.type == "Video":
                    return None
        else:
            return None, None
    
    def parse_duration(self):
        return None
    
    def __setattr__(self, attr, value) -> None:
        if attr == "id":
            super().__setattr__(attr, value)
            self.storage = self.parse_storage()
            self.type = self.parse_type()
            self.format = self.parse_format()
            self.height, self.width = self.parse_dimensions()
            self.duration = self.parse_duration()
        else:
            super().__setattr__(attr, value)
