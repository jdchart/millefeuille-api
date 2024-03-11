import mfapi

#media_url = "https://files.tetras-libre.fr/media/sceno_avignon.jpg"
# media_url = "https://filebrowser.tetras-libre.fr/files/www/media/test_markeas.wav"
media_url = "https://filebrowser.tetras-libre.fr/files/www/media/re_walden_full.mp4"

manifest = mfapi.Manifest()
manifest.add_canvas_from_media(media_url)


annotation_page = manifest.add_annotation_page()


annotation_page.add_annotation(
    label = "hello world",
    x = 20,
    y = 50,
    start = 0
)


manifest.to_json()