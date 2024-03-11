import os

class AnnotationPage():
    def __init__(self, canvas, manifest) -> None:
        self.canvas = canvas
        self.manifest = manifest
        self.items = []
        self.id = os.path.join(self.canvas.id, "annotation", "1")

    def add_annotation(self, **kwargs):
        ret = Annotation(self, len(self.items), **kwargs)
        self.items.append(ret)
        return ret
    
    def to_dict(self):
        ret = {
            "id" : self.id,
            "items" : [],
            "type": "AnnotationPage",
            "label": None,
            "context": None,
            "rendering": None,
            "service": None,
            "thumbnail": None,
        }
        for item in self.items:
            ret["items"].append(item.to_dict())
        return ret

class Annotation():
    def __init__(self, annotation_page, index, **kwargs) -> None:
        self.annotation_page = annotation_page
        self.index = index

        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)
        self.w = kwargs.get("w", None)
        self.h = kwargs.get("h", None)
        self.start = kwargs.get("start", None)
        self.end = kwargs.get("end", None)
        self.link_to_manifest = kwargs.get("link_to_manifest", None)
        self.label = kwargs.get("label", None)

        self.id = self.get_id()
        self.target = self.get_target()

    def to_dict(self):
        return {
            "id" : self.id,
            "target" : self.target,
            "motivation" : "commenting",
            "type": "Annotation",
            "label": None,
            "service": None,
            "rendering": None,
            "thumbnail": None,
            "body" : {
                "value" : self.label,
                "type" : "Image",
                "format" : "image/jpg",
                "id" : self.annotation_page.manifest.id
            }
        }

    def get_id(self):
        ret = os.path.join(self.annotation_page.id, str(self.index + 1))
        if self.link_to_manifest != None:
            ret = f"{ret}#{self.link_to_manifest}"
        return ret
    
    def get_target(self):
        ret = self.annotation_page.canvas.id
        xywh_string = self.get_xywh_string()
        t_string = self.get_t_string()

        if xywh_string != None and t_string == None:
            ret = f"{ret}#xywh={xywh_string}"
        elif xywh_string == None and t_string != None:
            ret = f"{ret}#t={t_string}"
        elif xywh_string != None and t_string != None:
            ret = f"{ret}#xywh={xywh_string}&t={t_string}"
        
        return ret

    def get_xywh_string(self):
        if self.x != None or self.y != None or self.w != None or self.h != None:
            if self.x == None:
                self.x = 0
            if self.y == None:
                self.y = 0
            if self.w == None:
                self.w = self.annotation_page.canvas.width
            if self.h == None:
                self.h = self.annotation_page.canvas.height
            return f"{self.x},{self.y},{self.w},{self.h}"
        else:
            return None
        
    def get_t_string(self):
        if self.start != None or self.end != None:
            if self.start == None:
                self.start = 0
            if self.end == None:
                self.end = self.annotation_page.canvas.duration
            return f"{self.start},{self.end}"
        else:
            return None