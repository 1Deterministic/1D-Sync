'''

This builds a log file to be written

'''

import _about
import _paths
import _strings

import os
import time

class Log:
    def __init__(self, root): # initializes an empty log
        self.path = os.path.join(root, _paths.logs_folder, time.strftime("%Y-%m-%d %H-%M-%S") + ".txt")
        self.error_occurred = False
        self.sync_occurred = False
        self.content = []

    def report(self, id, detail="", critical=False): # reports events in the log
        # writes the string associated to the received id
        # detail is used to include extra information in the message
        # critical is used to make sure the log is written right away when a serious error occurred
        try:
            self.content.append(_strings.strings[id] + detail)
        except:
            self.content.append(id + detail)

        if critical:
            return self.write()

        return True

    def write(self): # writes the message to the file system
        try:
            self.file = open(self.path, "w")
            self.file.write("        " + _about.name + " " + _about.version + " \"" + _about.codename + "\" build date:" + _about.build_date + "\n\n")

            for c in self.content:
                self.file.write(c + "\n")

            self.file.close()

            return True
        except:
            return False


