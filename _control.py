'''

This controls the sync scheduling

'''

import _paths

import os
import json
import datetime

class Control:
    def __init__(self, root): # test in Tests/Unit/test_control.test_init
        self.path = os.path.join(root, _paths.config_folder, _paths.control_file) # stores the path to the schedule file

    # loads the schedule file
    def load(self, log): # test in Tests/Unit/test_control.test_load
        try:
            self.properties = json.loads(open(self.path, "r", encoding="utf-8").read())
            log.report("ok_control_json_load")
            return True
        except:
            log.report("error_control_opening", critical=True)
            return False

    # given a sync name, tells if its time to run it
    def its_time(self, name): # test in Tests/Unit/test_control.test_its_time
        return datetime.datetime.now() > datetime.datetime.strptime(self.properties[name], "%Y-%m-%d %H-%M-%S")

    # schedules a sync to occur in time seconds from now
    def schedule(self, name, time): # test in Tests/Unit/test_control.test_schedule
        self.properties[name] = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H-%M-%S")
        return True

    # writes the changes back to the schedule file
    def write(self, log): # test in Tests/Unit/test_control.test_write
        try:
            with open(self.path, "w") as file_to_write:
                json.dump(self.properties, file_to_write, indent=4, ensure_ascii=False)

            log.report("ok_control_write")
            return True
        except:
            log.report("error_control_write", critical=True)
            return False