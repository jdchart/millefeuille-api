import os
from .utils import get_online_image_dims, get_tetras_url
from .data import media_types

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
        if self.id != None:
            for attr in self.__dict__:
                if attr != "storage":
                    if getattr(self, attr) != None:
                        ret[attr] = getattr(self, attr)
            return ret
        else:
            return None

    def parse_storage(self):
        if self.id != None:
            if self.id[:4] == "http":
                if self.id[:46] == "https://filebrowser.tetras-libre.fr/files/www/":
                    return "tetras"
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
            elif self.storage == "tetras":
                url = get_tetras_url(self.id)
                if self.type == "Image":
                    return get_online_image_dims(url)
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