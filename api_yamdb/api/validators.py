import re

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
