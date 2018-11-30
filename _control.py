'''

This controls the sync scheduling

'''

import _paths

import os
import json
import datetime

class Control:
    def __init__(self, root):
        self.path = os.path.join(root, _paths.config_folder, _paths.control_file) # stores the path to the schedule file

    def load(self, log): # loads the schedule file
        try:
            self.properties = json.loads(open(self.path, "r", encoding="utf-8").read())
            log.report("ok_control_json_load")
            return True
        except:
            log.report("error_control_opening", critical=True)
            return False

    def its_time(self, name): # given a sync name, tells if its time to run it
        return datetime.datetime.now() > datetime.datetime.strptime(self.properties[name], "%Y-%m-%d %H-%M-%S")

    def schedule(self, name, time): # schedules a sync to occur in time hours from now
        self.properties[name] = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H-%M-%S")
        return True

    def write(self, log): # writes the changes back to the schedule file
        try:
            with open(self.path, "w") as file_to_write:
                json.dump(self.properties, file_to_write, indent=4, ensure_ascii=False)

            log.report("ok_control_write")
            return True
        except:
            log.report("error_control_write", critical=True)
            return False