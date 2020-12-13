import os
from datetime import datetime

from django.utils.text import slugify

def unique_slug(manager, slug_field, slug):
    """
    Codigo extraido de https://github.com/stephenmcd/django-forms-builder
    Ensure slug is unique for the given manager, appending a digit
    if it isn't.
    """
    max_length = manager.model._meta.get_field(slug_field).max_length
    slug = slug[:max_length]
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            # We need to keep the slug length under the slug fields max length. We need to
            # account for the length that is added by adding a random integer and `-`.
            slug = "%s-%s" % (slug[:max_length - len(str(i)) - 1], i)
        if not manager.filter(**{slug_field: slug}):
            break
        i += 1
    return slug