'''

This implements the basic validations used by the program

'''

import os

def validate_path(path):
    return os.path.isdir(path)

def validate_boolean_value(value):
    return value == "True" or value == "False"

def validate_integer_greater_than_or_equal_to_zero(value):
    try:
        return int(value) >= 0
    except:
        return False

def validate_integer_greater_than_zero(value):
    try:
        return int(value) > 0
    except:
        return False

def validate_selection_condition(condition):
    return True