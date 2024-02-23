from .manifest import MediaBody

def test_media(path : str):
    """
    Provide the url or a path to a media file and test if it can be accessed.
    
    If it can be accessed the function will return a dict giving the media file's information,
    if the test fails it will return None.
    """
    try:
        media_body = MediaBody(id = path)
        return media_body.to_dict()
    except:
        return None