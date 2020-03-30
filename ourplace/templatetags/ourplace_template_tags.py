from django import template

register = template.Library()

@register.inclusion_tag('ourplace/place_carousel.html')
def display_carousel(place_list=None, include_author=True):
    return {'place_list':place_list,
            'include_author': include_author}
