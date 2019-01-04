import unittest

import _validations

class TestValidations(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_path(self):
        valid_paths = ["Tests/Unit"]
        invalid_paths = ["Tests/UnitWRONG"]

        for valid_path in valid_paths:
            self.assertTrue(_validations.validate_path(valid_path))

        for invalid_path in invalid_paths:
            self.assertFalse(_validations.validate_path(invalid_path))

    def test_validate_boolean_value(self):
        valid_booleans = ["True"]
        invalid_booleans = ["TrueWRONG"]

        for valid_boolean in valid_booleans:
            self.assertTrue(_validations.validate_boolean_value(valid_boolean))

        for invalid_boolean in invalid_booleans:
            self.assertFalse(_validations.validate_boolean_value(invalid_boolean))

    def test_validate_integer_greater_than_or_equal_to_zero(self):
        valid_integers = ["15"]
        invalid_integers = ["-41"]

        for valid_integer in valid_integers:
            self.assertTrue(_validations.validate_integer_greater_than_or_equal_to_zero(valid_integer))

        for invalid_integer in invalid_integers:
            self.assertFalse(_validations.validate_integer_greater_than_or_equal_to_zero(invalid_integer))

    def test_validate_integer_greater_than_zero(self):
        valid_integers = ["15"]
        invalid_integers = ["0"]

        for valid_integer in valid_integers:
            self.assertTrue(_validations.validate_integer_greater_than_zero(valid_integer))

        for invalid_integer in invalid_integers:
            self.assertFalse(_validations.validate_integer_greater_than_zero(invalid_integer))

    def test_validate_selection_condition(self):
        valid_conditions = ["a ^ b | ~{c ^ ~d}"]
        invalid_conditions = ["a ^ b | ~{c ^ ~d"]

        for valid_condition in valid_conditions:
            self.assertTrue(_validations.validate_selection_condition(valid_condition))

        for invalid_condition in invalid_conditions:
            self.assertFalse(_validations.validate_selection_condition(invalid_condition))

if __name__ == '__main__':
    unittest.main()