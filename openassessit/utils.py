import re

# Custom filter for jinja
def generate_img_filename(url, identifier):
    return re.sub(r'\W', '-', '%s%s' % (url, identifier)) + '.png'