from django import template

register = template.Library()


@register.filter(name='pn')
def persian_numbers(value):
    value = str(value)
    english_to_persian_table = value.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹,')
    return value.translate(english_to_persian_table)


@register.filter(name='cspn')
def comma_separated_persian_numbers(value, separator=3):
    try:
        s = int(separator)
        separator = s if s>0 else 3
    except ValueError:
        separator = 3
    value = str(value)
    value = value.replace(',', '')
    value = value.replace('_', '')
    if len(value)==0:
        raise ValueError("The parameter you sent is empty!")
    for digit in value:
        if digit not in '0123456789۰۱۲۳۴۵۶۷۸۹':
            raise ValueError("The parameter you sent is not a real number!")
    res = ''
    for i, char in enumerate(value[::-1]):
        res += char
        if i%separator==separator-1:
            res+=','
    if i%separator==separator-1:
        value = res[-2::-1]
    else:
        value = res[::-1]
    table = value.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return value.translate(table)
