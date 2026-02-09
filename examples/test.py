import mfapi
import json
import requests


src_data_url = "https://files.tetras-libre.fr/media/plozevet/fonds_gessain/plozevet_sources_metadata.json"

response = requests.get(src_data_url)
if response.status_code == 200:
    src_list = json.loads(response.text)

print(src_list)




MANIFEST_PATH = "manifests/plozevet/sources"

for item in src_list:
    src = src_list[item]
    print("Creating Manifest for " + src["url"] + " (" + src["metadata"][0]["value"] + ")...")

    manifest = mfapi.Manifest(manifest_path = MANIFEST_PATH, logo = "https://mediatheque.landerneau.bzh/medias/sites/3/2019/12/logo_CDB_1.jpg")
    manifest.label = {"en" : [src["metadata"][0]["value"]]}
    manifest.requiredStatement = {"label": {"en": ["Attribution"]}, "value": {"en": ["Cinématèque de Bretagne"]}}
    manifest.provider = [{
        "id": "https://www.cinematheque-bretagne.bzh/",
        "type": "Agent",
        "label": {"en": ["Cinématèque de Bretagne"]},
        "homepage": [{
                    "id": "https://www.cinematheque-bretagne.bzh/",
                    "type": "Text",
                    "label": {"en": ["Cinématèque de Bretagne"]},
                    "format": "text/html"
                    }]
        }]

    for meta in src["metadata"]:
        manifest.add_metadata({"en" : [meta["label"]]}, {"en" : [str(meta["value"])]})
    manifest.add_metadata({"en" : ["Index"]}, {"en" : [item]})

    manifest.add_canvas_from_media(src["url"])

    print(manifest.to_dict())