'''

This implements the basic validations used by the program

'''

import os

from Slea import slea

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

# possibly add a log entry
def validate_selection_condition(condition):
    error_code = slea.evaluate_syntax(condition)
    if error_code == len(condition):
        return True
    else:
        return False