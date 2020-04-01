from django import template

register = template.Library()

@register.inclusion_tag('ourplace/place_carousel.html')
def display_carousel(place_list, user):
    return_dict = {'place_list': place_list, 'user':user}
    return return_dict

@register.inclusion_tag('ourplace/styled_form.html')
def styled_form(form):
    return_dict = {'form': form}
    if len(list(form)) == 1:
        return_dict['single_input'] = [input for input in form][0]
    return return_dict
