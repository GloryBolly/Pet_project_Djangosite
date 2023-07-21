from django import template

from todolist.models import *

register = template.Library()

@register.simple_tag()
def get_all_categories():
    return Category.objects.all()
