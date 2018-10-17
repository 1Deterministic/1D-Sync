'''

This stores information about a file
Also implements every action related to files

'''

import _filetypes

import os
import shutil
import eyed3
import math
import time
import filecmp

class File:
    def __init__(self, path): # reads information about the file on a given path
        try:
            self.path = path
            self.islink = os.path.islink(path)
            self.size = os.path.getsize(self.path) / 1024000
            self.age = int(time.strftime("%d", time.gmtime(time.time() - os.path.getmtime(self.path))))
            self.basename = os.path.basename(self.path)
            self.extension = os.path.splitext(self.path)[1]
            self.to_copy = True
            self.to_delete = False
        except: # erases all information in case of an error
            self.path = ""
            self.islink = False
            self.size = 0.0
            self.age = 0
            self.basename = ""
            self.extension = ""
            self.to_copy = False
            self.to_delete = False

    def is_the_same_file(self, other):
        return filecmp.cmp(self.path, other.path)


    def copy(self, destination, log): # copies this file to a given target folder
        if self.to_copy and (not self.path == ""):
            try:
                if not os.path.isdir(destination):
                    os.makedirs(destination) # will build all directory tree if the destination is not a folder

                shutil.copy(self.path, destination)

                log.report("ok_file_copy", detail=self.path)
                return True
            except:
                log.report("error_file_copy", detail=self.path)
                return False

        return True

    def delete(self, log): # removes this file from the filesystem
        if self.to_delete and (not self.path == ""):
            try:
                os.remove(self.path)
                log.report("ok_file_delete", detail=self.path)

                self.path = ""
                self.islink = False
                self.size = 0.0
                self.age = 0
                self.basename = ""
                self.extension = ""
                return True
            except:
                log.report("error_file_delete", detail=self.path)
                return False

        return True

    def evaluate_type(self, filetype):
        types = filetype.split("|")
        for t in types:
            if _filetypes.condition_check(t, self.path):
                return True

        return False

    def evaluate_age(self, age): # tells if this file is younger than the maximum age
        if age == "any age":
            return True
        else:
            try:
                return self.age <= int(age)
            except:
                return False