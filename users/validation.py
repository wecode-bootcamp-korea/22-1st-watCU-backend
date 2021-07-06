import re

email_regex     = '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$'
password_regex  = '[0-9a-zA-Z\!\@\#\?]{8,20}'

def email_validation(email):
    return re.match(email_regex, email)

def password_validation(password):
    return re.match(password_regex, password)
