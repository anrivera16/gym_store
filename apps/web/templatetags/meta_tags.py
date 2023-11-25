from django import template
from django.conf import settings
from django.template.defaulttags import url
from django.templatetags.static import static

from apps.web import meta

register = template.Library()


@register.filter
def get_title(project_meta, page_title=None):
    if page_title:
        return "{} | {}".format(page_title, project_meta["NAME"])
    else:
        return project_meta["TITLE"]


@register.filter
def get_description(project_meta, page_description=None):
    return page_description or project_meta["DESCRIPTION"]


@register.filter
def get_image_url(project_meta, page_image=None):
    if page_image and page_image.startswith("/"):
        # if it's a local media url make it absolute, otherwise assume static
        if page_image.startswith(settings.MEDIA_URL):
            page_image = meta.absolute_url(page_image)
        else:
            page_image = meta.absolute_url(static(page_image))

    return page_image or project_meta["IMAGE"]


@register.simple_tag
def absolute_url(path):
    return meta.absolute_url(path)
