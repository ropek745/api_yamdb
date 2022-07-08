import re

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import USERNAME_SYMBOLS

SYMBOLS_ERROR = 'Недопустимые символы: {value}.'


class UserValidator:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(f'Недопустимое имя пользователя !{value}')
        if not re.match(USERNAME_SYMBOLS, value):
            raise ValidationError(
                SYMBOLS_ERROR.format(
                    value=[
                        symbol for symbol in value if symbol not in ''.join(
                            re.findall(USERNAME_SYMBOLS, value)
                        )
                    ]
                )
            )
        return value


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} год еще не наступил!',
        )