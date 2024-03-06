import mfapi

media_url = "https://files.tetras-libre.fr/manifests/fsa_color/1a33888v.json"

loaded = mfapi.read_manifest(media_url).get_media().id


img = mfapi.read_manifest(media_url).media_to_np()


print(img)