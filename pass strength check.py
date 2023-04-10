import re

def check_password_strength(password):
    if len(password) < 8:
        return "Weak"
    elif re.search('[0-9]', password) is None:
        return "Weak"
    elif re.search('[a-z]', password) is None:
        return "Weak"
    elif re.search('[A-Z]', password) is None:
        return "Weak"
    elif re.search('[!@#$%^&*()_+-=]', password) is None:
        return "Weak"
    else:
        return "Strong"