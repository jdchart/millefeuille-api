import mfapi

#media_url = "https://files.tetras-libre.fr/media/sceno_avignon.jpg"

media_url = "https://filebrowser.tetras-libre.fr/files/www/media/test_markeas.wav"
media_url = "https://filebrowser.tetras-libre.fr/files/www/media/re_walden_full.mp4"

manifest = mfapi.Manifest()


manifest.add_canvas_from_media(media_url)


manifest.add_metadata({"en" : ["Country"]}, {"en" : ["France"]})
manifest.add_metadata({"en" : ["Date"]}, {"en" : ["2024"]})

manifest.print()