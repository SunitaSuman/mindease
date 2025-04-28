from django import template

register = template.Library()

@register.filter
def replace(value, args):
    old, new = args.split(',')
    return value.replace(old.strip(), new.strip())

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for the given key"""
    return dictionary.get(key)



@register.filter
def mood_count(moods, mood_type):
    """Count occurrences of a specific mood type"""
    return moods.filter(mood=mood_type).count()

@register.filter
def percentage(value, total):
    """Calculate percentage"""
    if total == 0:
        return 0
    return int((value / total) * 100)

@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    return float(value) * float(arg)