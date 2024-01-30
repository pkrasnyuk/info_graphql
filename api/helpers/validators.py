from django.core.validators import RegexValidator


def alphanumeric(value):
    RegexValidator(r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed.")(value)


def letters_only(value):
    RegexValidator(r"^[a-zA-Z]*$", "Only letters characters are allowed.")(value)
