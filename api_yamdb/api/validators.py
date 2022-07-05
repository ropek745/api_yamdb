import re

from rest_framework.exceptions import ValidationError

SYMBOLS = re.compile(r'[\w.@+-@./+-]+')
SYMBOLS_ERROR = 'Недопустимые символы: {value}.'


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    if not re.match(SYMBOLS, value):
        raise ValidationError(
            SYMBOLS_ERROR.format(
                value=[
                    symbol for symbol in value if symbol not in ''.join(
                        re.findall(SYMBOLS, value)
                    )
                ]
            )
        )
    return value
