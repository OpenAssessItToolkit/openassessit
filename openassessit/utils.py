import re

def generate_img_filename(url, identifier):
    """generate useful filename with a max of 260 chars"""
    return re.sub(r'\W', '-', '%s%s' % (url[0:36], identifier[-210:])) + '.png'