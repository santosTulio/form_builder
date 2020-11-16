import os
from datetime import datetime

from django.utils.text import slugify

def content_file_name(obj, file):
    name, ext = os.path.splitext(file)
    return os.path.join( 'upload', '/'.join([obj._meta.app_label,obj.__class__.__name__]), slugify(name[:50])+ext )