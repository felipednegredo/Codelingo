import re
from django.core.exceptions import ValidationError

def alphanumeric_password_validator(value):
    if not re.match(r'^[a-zA-Z0-9]{8,20}$', value):
        raise ValidationError(
            'A senha deve ser alfanumérica e ter entre 8 e 20 caracteres.'
        )