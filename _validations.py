'''

This implements the basic validations used by the program

'''

import os

from Slea import slea

def validate_path(path): # test in Tests/Unit/test_validations.test_validate_path
    return os.path.isdir(path)

def validate_boolean_value(value): # test in Tests/Unit/test_validations.test_validate_boolean_value
    return value == "True" or value == "False"

def validate_integer_greater_than_or_equal_to_zero(value): # test in Tests/Unit/test_validations.test_validate_integer_greater_than_or_equal_to_zero
    try:
        return int(value) >= 0
    except:
        return False

def validate_integer_greater_than_zero(value): # test in Tests/Unit/test_validations.test_validate_integer_greater_than_zero
    try:
        return int(value) > 0
    except:
        return False

# possibly add a log entry
def validate_selection_condition(condition): # test in Tests/Unit/test_validations.test_validate_selection_condition
    return slea.evaluate_syntax(condition) == len(condition)