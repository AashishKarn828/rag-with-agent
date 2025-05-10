import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError

def validate_name(name):
    return bool(name.strip())

def validate_email_input(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_phone(phone):
    try:
        number = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(number)
    except:
        return False
