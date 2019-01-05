import unittest
import os

import _log
import _defaults
import _about
import _strings

class TestLog(unittest.TestCase):
    def setUp(self):
        for (dirpath, dirnames, filenames) in os.walk("Tests/Temp"):
            for f in filenames:
                os.remove(os.path.join(dirpath, f))

        for (dirpath, dirnames, filenames) in os.walk("Tests/Temp"):
            for d in dirnames:
                if not dirpath == d:
                    os.rmdir(os.path.join(dirpath, d))

        if not os.path.isdir("Tests/Temp/Logs"):
            os.mkdir("Tests/Temp/Logs")

    def test_init(self):
        log = _log.Log("Tests/Temp")

        self.assertTrue(log.path.startswith("Tests/Temp"))
        self.assertTrue(log.path.endswith(".txt"))

        self.assertFalse(log.error_occurred)
        self.assertFalse(log.warning_occurred)
        self.assertFalse(log.sync_occurred)

        self.assertEqual(log.content, [])
        self.assertEqual(log.summary, [])

        self.assertEqual(log.repeated_line, "")
        self.assertEqual(log.repeated_count, 0)

    def test_report(self):
        # will test all strings in all languages
        for language in _strings.languages:
            _strings.strings = _strings.languages[language]

            for string in _strings.strings.keys():
                if string.startswith("email"):
                    continue

                log = _log.Log(".")
                detail = "test"
                log.report(string, detail=detail)

                if string.startswith("ok"):
                    self.assertFalse(log.error_occurred)
                    self.assertFalse(log.warning_occurred)
                    self.assertFalse(log.sync_occurred)

                elif string.startswith("warning"):
                    self.assertFalse(log.error_occurred)
                    self.assertTrue(log.warning_occurred)
                    self.assertFalse(log.sync_occurred)

                elif string.startswith("error"):
                    self.assertTrue(log.error_occurred)
                    self.assertFalse(log.warning_occurred)
                    self.assertFalse(log.sync_occurred)

                elif string.startswith("message"):
                    self.assertFalse(log.error_occurred)
                    self.assertFalse(log.warning_occurred)
                    self.assertFalse(log.sync_occurred)

                elif string.startswith("prefix"):
                    self.assertFalse(log.error_occurred)
                    self.assertFalse(log.warning_occurred)
                    self.assertFalse(log.sync_occurred)

    def test_insert(self):
        # will test all strings in all languages
        for language in _strings.languages:
            _strings.strings = _strings.languages[language]

            for string in _strings.strings.keys():
                if string.startswith("email"):
                    continue

                log = _log.Log(".")
                detail = "test"
                log.insert(string, detail=detail)
                self.assertEqual(log.content[0][18:], _strings.strings[string] + detail)

    def test_get_content(self):
        log = _log.Log(".")
        log.content = ["test"]
        self.assertEqual(log.get_content(), _strings.strings["prefix_timestamp_spacing"] + _strings.strings["prefix_spacing"] + _about.name + " " + _about.version + " \"" + _about.codename + "\" build date:" + _about.build_date + "\n\ntest\n")

    def test_write(self):
        log = _log.Log("Tests/Temp")
        log.content = ["test"]
        log.write()
        fl = open(log.path, "r")
        text = fl.read()
        fl.close()
        self.assertEqual(text, _strings.strings["prefix_timestamp_spacing"] + _strings.strings["prefix_spacing"] + _about.name + " " + _about.version + " \"" + _about.codename + "\" build date:" + _about.build_date + "\n\ntest\n")


if __name__ == '__main__':
    unittest.main()