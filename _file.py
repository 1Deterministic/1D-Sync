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

    def evaluate_type(self, filetype): # tells if this file is a filetype (if it is an image file, an audio file, a document file...)
        evaluations = {
            # multimedia
            "audio": lambda: _filetypes.audio_extensions.__contains__(self.extension),
            "image": lambda: _filetypes.image_extensions.__contains__(self.extension),
            "video": lambda: _filetypes.video_extensions.__contains__(self.extension),

            # office
            "document": lambda: _filetypes.document_extensions.__contains__(self.extension),
            "sheet": lambda: _filetypes.sheet_extensions.__contains__(self.extension),
            "presentation": lambda: _filetypes.presentation_extensions.__contains__(self.extension),

            # any or none
            "any file": lambda: True,
            "none": lambda: False,

            # favorite audio requires a different approach
            "favorite audio": lambda: self.extension == ".mp3" and Tag(self.path).rating == 5
        }

        conditions = filetype.split(";") # filetype can have multiple values separated by ;

        try:
            for c in conditions:
                if evaluations.get(c)(): # if any possible type is satisfied, return True
                    return True

            return False
        except:
            return False

    def evaluate_age(self, age): # tells if this file is younger than the maximum age
        if age == "any age":
            return True
        else:
            try:
                return self.age <= int(age)
            except:
                return False



class Tag: # this helps dealing with mp3 files (for the favorite audio evaluation)
    def __init__(self, path):
        try:
            self.file = eyed3.load(path)
            self.artist = self.file.tag.artist
            self.album = self.file.tag.album
            self.title = self.file.tag.title
            self.rating = math.ceil(self.file.tag.frame_set[b'POPM'][0].rating / 51)
        except:
            self.artist = "<none>"
            self.album = "<none>"
            self.title = "<none>"
            self.rating = 0