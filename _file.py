'''

This stores information about a file
Also implements every action related to files

'''

import _defaults

import os
import shutil
import eyed3
import math
import time
import filecmp
import magic
from Slea import slea


class File:
    def __init__(self, path): # reads information about the file on a given path
        try:
            self.path = path
            self.islink = os.path.islink(path)
            self.size = os.path.getsize(self.path) / 1024000
            self.basename = os.path.basename(self.path)
            self.extension = os.path.splitext(self.path)[1]
            self.age = int(time.strftime("%d", time.gmtime(time.time() - os.path.getmtime(self.path))))
            self.to_copy = True
            self.to_delete = False
            self.tag = Tag()

        except: # erases all information in case of an error
            self.path = ""
            self.islink = False
            self.size = 0.0
            self.basename = ""
            self.extension = ""
            self.age = 0
            self.to_copy = False
            self.to_delete = False
            self.tag = Tag()

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
                self.basename = ""
                self.extension = ""
                return True
            except:
                log.report("error_file_delete", detail=self.path)
                return False

        return True

    def evaluate_condition(self, condition, argument):
        # argument is an optional argument for slea
        # it isn't used but the function must have it

        # restore spaces
        actual_condition = condition.replace(_defaults.default_space_symbol_placeholder, " ")

        # ext
        if actual_condition.startswith("ext:"):
            return self.extension == actual_condition.split(":", 1)[1]

        # type
        elif actual_condition.startswith("type:"):
            return magic.Magic(mime=True).from_file(self.path).startswith(actual_condition.split(":", 1)[1])

        # eyed3
        elif actual_condition.startswith("eyed3:"):
            string = actual_condition.split(":", 1)[1]

            if not self.tag.loaded:
                if not self.tag.load(self.path):
                    return False

            if string.startswith("artist:"):
                return self.tag.artist == string.split(":", 1)[1]

            elif string.startswith("album:"):
                return self.tag.album == string.split(":", 1)[1]

            elif string.startswith("title:"):
                return self.tag.title == string.split(":", 1)[1]

            elif string.startswith("rating:"):
                str = string.split(":", 1)[1]

                cmp = str.split(":", 1)[0]
                ref = str.split(":", 1)[1]
                return self.condition_compare_int(self.tag.rating, cmp, ref)

            return False

        # age
        elif actual_condition.startswith("age:"):
            string = actual_condition.split(":", 1)[1]

            cmp = string.split(":", 1)[0]
            ref = string.split(":", 1)[1]
            return self.condition_compare_int(self.age, cmp, ref)

        # generic
        elif actual_condition == "anyfile":
            return True

        elif actual_condition == "none":
            return False

        # could not validate
        else:
            return False

    # compares two values and return according to a received condition
    def condition_compare_int(self, value_a, cmp, value_b):
        try:
            a = int(value_a)
            b = int(value_b)

            if cmp == "=":
                return a == b
            if cmp == "~":
                return not a == b
            if cmp == ">":
                return a > b
            if cmp == "<":
                return a < b
            if cmp == ">=":
                return a >= b
            if cmp == "<=":
                return a <= b
        except:
            return False


class Tag:
    def __init__(self):
        self.loaded = False

    def load(self, path):
        try:
            self.file = eyed3.load(path)

            self.title = self.file.tag.title;
            self.album = self.file.tag.album;
            self.artist = self.file.tag.artist;
            self.rating = math.ceil(self.file.tag.frame_set[b'POPM'][0].rating / 51)

            self.loaded = True
            return True
        except:
            return False
