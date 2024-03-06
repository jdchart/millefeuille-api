import mfapi

#media_url = "https://filebrowser.tetras-libre.fr/files/www/media/sceno_avignon.jpg"
#media_url = "https://files.tetras-libre.fr/media/sceno_avignon.jpg"

media_url = "https://filebrowser.tetras-libre.fr/files/www/media/test_markeas.wav"
#media_url = "https://filebrowser.tetras-libre.fr/files/www/media/re_walden_full.mp4"



result = mfapi.media_test(media_url)
print(result)