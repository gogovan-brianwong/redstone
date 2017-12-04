import os
from dao.models import AppName
from django import template
from django.shortcuts import render, HttpResponse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@register.simple_tag
def customize(app_id, app_name):

    obj = AppName.objects.filter(id=app_id).all()
    for row in obj:

        ret = render_to_string(row.custom_tab_html)
        return format_html(mark_safe(ret))