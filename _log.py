'''

This builds a log file to be written

'''

import _about
import _paths
import _strings
import _defaults

import os
import time

class Log:
    def __init__(self, root): # initializes an empty log
        self.path = os.path.join(root, _paths.logs_folder, time.strftime("%Y-%m-%d %H-%M-%S") + ".txt")
        self.error_occurred = False
        self.warning_occurred = False
        self.sync_occurred = False
        self.content = []

        self.repeated_line = ""
        self.repeated_count = 0

    def report(self, id, detail="", critical=False): # reports events in the log
        # writes the string associated to the received id
        # detail is used to include extra information in the message
        # critical is used to make sure the log is written right away when a serious error occurred
        if id.startswith("error"):
            self.error_occurred = True

        if id.startswith("warning"):
            self.warning_occurred = True

        if (id + detail) == self.repeated_line:
            self.repeated_count += 1

            if self.repeated_count <= _defaults.default_log_repeated_lines_threshold:
                try:
                    self.insert(id, detail)
                except:
                    # log the raw string if it was not identified
                    self.insert(id, detail)

        else:
            if self.repeated_count > _defaults.default_log_repeated_lines_threshold:
                self.insert("message_repeated_lines", str(self.repeated_count - _defaults.default_log_repeated_lines_threshold))

            self.repeated_count = 0
            self.repeated_line = id + detail

            try:
                self.insert(id, detail)
            except:
                # log the raw string if it was not identified
                self.insert(id, detail)


        if critical:
            return self.write()

        return True

    def insert(self, id, detail):
        if id.startswith("ok"):
            self.content.append(_strings.strings["prefix_ok"] + _strings.strings[id] + detail)
        elif id.startswith("error"):
            self.content.append(_strings.strings["prefix_error"] + _strings.strings[id] + detail)
        elif id.startswith("warning"):
            self.content.append(_strings.strings["prefix_warning"] + _strings.strings[id] + detail)
        elif id.startswith("message"):
                self.content.append(_strings.strings[id] + detail)

        else:
            self.content.append(id + detail)


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


