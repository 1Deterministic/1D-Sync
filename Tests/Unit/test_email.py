import unittest

import _email
import _log

class TestEmail(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        email = _email.Email()
        self.assertEqual(email.message, "")

    def test_send(self):
        email = _email.Email()
        log = _log.Log("Tests/Temp")
        self.assertFalse(email.send("#####@gmail.com", "strong and complicated password", "#####@gmail.com", log))
        self.assertTrue(log.error_occurred)

    def test_append_message(self):
        email = _email.Email()
        email.append_message("test")
        self.assertEqual(email.message, "test")


if __name__ == '__main__':
    unittest.main()