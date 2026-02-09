import mfapi
import os
import shutil
import json

PATH_ON_SERVER = "manifests/plozevet/sources"

if os.path.isdir("manifests_out"):
  shutil.rmtree("manifests_out")
os.makedirs("manifests_out")

for analysis_result_path in os.listdir("analysis_results"):
  
  # Retrieve analysis results as a dict:
  with open(os.path.join("analysis_results", analysis_result_path), 'r') as f:
    analysis_results = json.load(f)

  full_manifest_path = os.path.join(PATH_ON_SERVER, os.path.splitext(os.path.basename(analysis_results["manifest_path"]))[0])
  os.makedirs(os.path.join("manifests_out", os.path.splitext(os.path.basename(analysis_results["manifest_path"]))[0]))
  
  # Load the original manifest to get the metadata:
  original_manifest = mfapi.read_manifest(analysis_results["manifest_path"])

  for i, shot_data in enumerate(analysis_results["shots"]):
    
    # Create a new Manifest:
    manifest = mfapi.Manifest(manifest_path = full_manifest_path, logo = "https://mediatheque.landerneau.bzh/medias/sites/3/2019/12/logo_CDB_1.jpg")
    manifest.label = {"en" : [original_manifest.label["en"][0] + f" : shot {i + 1}/" + str(len(analysis_results["shots"]))]}
    manifest.metadata = original_manifest.metadata
    manifest.requiredStatement = original_manifest.requiredStatement
    manifest.provider = original_manifest.provider

    manifest.add_canvas_from_media(analysis_results["media_path"], start = shot_data[0], end = shot_data[1])

    with open(os.path.join("manifests_out", os.path.splitext(os.path.basename(analysis_results["manifest_path"]))[0], manifest.uuid + ".json"), 'w', encoding='utf-8') as f:
      json.dump(manifest.to_dict(), f, ensure_ascii = False, indent = 2)
  