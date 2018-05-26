import _about

# class for dealing with logs
class Log:
    def __init__(self, path):
        # the log strings are stored as elements of a list
        self.content = []
        # the path
        self.path = path
        # the file object
        self.file = None

    # opens the log file for write at the path received
    def open(self):
        try:
            self.file = open(self.path, "w")
            return True

        except:
            return False


    # adds an entry on the list
    def report(self, text):
        self.content.append(text)

        return True


    # writes the list to the file and closes the file and the log
    def write(self):
        self.file.write("        " + _about.PROGRAM_NAME + " " + _about.PROGRAM_VERSION + " build date:" + _about.PROGRAM_BUILD_DATE + "\n\n")
        for c in self.content:
            self.file.write(c + "\n")

        # closes the file
        self.file.close()

        # erases the properties of this object
        self.content = []
        self.path = ""
        self.file = None

        return True
