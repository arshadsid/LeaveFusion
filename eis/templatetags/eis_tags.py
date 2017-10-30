from django import template

register = template.Library()

def get_remainder(num):
    return (num%10)

register.inclusion_tag(get_remainder)