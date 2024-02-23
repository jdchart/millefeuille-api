import mfapi

#media_url = "https://filebrowser.tetras-libre.fr/files/www/media/sceno_avignon.jpg"
media_url = "https://files.tetras-libre.fr/media/sceno_avignon.jpg"

result = mfapi.media_test(media_url)
print(result)