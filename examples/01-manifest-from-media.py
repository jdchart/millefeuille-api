import mfapi

manifest = mfapi.Manifest()

print(manifest.label)
print(manifest.uuid)


manifest.add_canvas_from_media("https://filebrowser.tetras-libre.fr/files/www/media/sceno_avignon.jpg")


manifest.add_metadata({"en" : ["Country"]}, {"en" : ["France"]})
manifest.add_metadata({"en" : ["Date"]}, {"en" : ["2024"]})

manifest.print()