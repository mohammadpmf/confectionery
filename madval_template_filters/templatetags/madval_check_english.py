from string import ascii_letters
from django import template

register = template.Library()


@register.filter(name='has_english_letter')
def has_english_letter(word: str):
    for char in word:
        if char in ascii_letters:
            return True
    return False    
