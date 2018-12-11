'''

This builds a log file to be written

'''

import _about
import _paths
import _strings
import _defaults

import os
import time
import datetime

class Log:
    def __init__(self, root): # initializes an empty log
        self.path = os.path.join(root, _paths.logs_folder, time.strftime("%Y-%m-%d %H-%M-%S") + ".txt")

        self.error_occurred = False
        self.warning_occurred = False
        self.sync_occurred = False

        self.content = []
        self.summary = []

        self.repeated_line = ""
        self.repeated_count = 0

    def report(self, id, detail="", critical=False): # reports events in the log
        if id.startswith("error"):
            self.error_occurred = True

        if id.startswith("warning"):
            self.warning_occurred = True

        if (id + detail) == self.repeated_line:
            self.repeated_count += 1

            if self.repeated_count <= _defaults.default_log_repeated_lines_threshold:
                self.insert(id, detail)

        else:
            if self.repeated_count > _defaults.default_log_repeated_lines_threshold:
                self.insert("message_repeated_lines", str(self.repeated_count - _defaults.default_log_repeated_lines_threshold))

            self.repeated_count = 0
            self.repeated_line = id + detail

            self.insert(id, detail)

        if critical:
            return self.write()

        return True

    def insert(self, id, detail):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")

        if id.startswith("ok"):
            self.content.append(timestamp + _strings.strings["prefix_ok"] + _strings.strings[id] + detail)
        elif id.startswith("error"):
            self.content.append(timestamp + _strings.strings["prefix_error"] + _strings.strings[id] + detail)
        elif id.startswith("warning"):
            self.content.append(timestamp + _strings.strings["prefix_warning"] + _strings.strings[id] + detail)
        elif id.startswith("message"):
            self.content.append(timestamp + _strings.strings[id] + detail)

        else:
            # skip timestamp in this case but include some spacing for indentation
            self.content.append(_strings.strings["prefix_timestamp_spacing"] + _strings.strings["prefix_spacing"] + id.replace("\n", "\n" + _strings.strings["prefix_timestamp_spacing"] + _strings.strings["prefix_spacing"]) + detail)

    def get_content(self):
        string = ""

        string += _strings.strings["prefix_timestamp_spacing"] + _strings.strings["prefix_spacing"] + _about.name + " " + _about.version + " \"" + _about.codename + "\" build date:" + _about.build_date + "\n\n"
        for c in self.content:
            string += c + "\n"

        return string

    def write(self): # writes the message to the file system
        try:
            self.file = open(self.path, "w")
            self.file.write(self.get_content())
            self.file.close()

            return True

        except:
            return False


