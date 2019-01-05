import unittest
import os
import datetime

import _control
import _log
import _paths

class TestControl(unittest.TestCase):
    def setUp(self):
        for (dirpath, dirnames, filenames) in os.walk("Tests/Temp"):
            for f in filenames:
                os.remove(os.path.join(dirpath, f))

        for (dirpath, dirnames, filenames) in os.walk("Tests/Temp"):
            for d in dirnames:
                if not dirpath == d:
                    os.rmdir(os.path.join(dirpath, d))

        if not os.path.isdir("Tests/Temp/Config"):
            os.mkdir("Tests/Temp/Config")

        if not os.path.isdir("Tests/Temp/Logs"):
            os.mkdir("Tests/Temp/Logs")

        control = open("Tests/Temp/Config/control.json", "w")
        control.write("""{
            "itstime.json": "2000-01-01 00-00-00",
            "notyet.json": "3000-01-01 00-00-00"            
        }""")
        control.close()

    def test_init(self):
        control = _control.Control("Tests/Temp")
        self.assertEqual(control.path, os.path.join("Tests/Temp", _paths.config_folder, _paths.control_file))


    def test_load(self):
        log = _log.Log("Tests/Temp")
        control = _control.Control("Tests/Temp")
        self.assertTrue(control.load(log))
        self.assertFalse(log.error_occurred)
        self.assertFalse(log.warning_occurred)
        self.assertFalse(log.sync_occurred)

        control = _control.Control("Tests/TempWRONG")
        self.assertFalse(control.load(log))
        self.assertTrue(log.error_occurred)
        self.assertFalse(log.warning_occurred)
        self.assertFalse(log.sync_occurred)

    def test_its_time(self):
        log = _log.Log("Tests/Temp")
        control = _control.Control("Tests/Temp")
        self.assertTrue(control.load(log))
        self.assertTrue(control.its_time("itstime.json"))
        self.assertFalse(control.its_time("notyet.json"))

    def test_schedule(self):
        log = _log.Log("Tests/Temp")
        control = _control.Control("Tests/Temp")
        self.assertTrue(control.load(log))
        now = datetime.datetime.now()
        control.schedule("itstime.json", 1)
        self.assertEqual(control.properties["itstime.json"], (now + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H-%M-%S"))

    def test_write(self):
        log = _log.Log("Tests/Temp")
        control = _control.Control("Tests/Temp")
        self.assertTrue(control.load(log))
        now = datetime.datetime.now()
        control.schedule("itstime.json", 1)
        self.assertTrue(control.write(log))
        self.assertFalse(log.error_occurred)
        self.assertFalse(log.warning_occurred)
        self.assertFalse(log.sync_occurred)
        self.assertTrue(os.path.isfile(control.path))

        log = _log.Log("Tests/Temp")
        log.path = "Tests/Temp/Logs/Error.txt"
        control = _control.Control("Tests/TempWRONG")
        self.assertFalse(control.load(log))
        self.assertFalse(control.write(log))
        self.assertTrue(log.error_occurred)
        self.assertFalse(log.warning_occurred)
        self.assertFalse(log.sync_occurred)
        # ensures that the log is written right away when needed (critical=True)
        self.assertTrue(os.path.isfile("Tests/Temp/Logs/Error.txt"))


if __name__ == '__main__':
    unittest.main()
