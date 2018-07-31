import _filetypes

import os
import shutil
import eyed3
import math
import time

class File:
    # creates a file object, containing some information
    def __init__(self, path):
        try:
            #self.path = str(pathlib.Path(path).resolve()) # path of the file resolved (will follow a symlink)
            self.path = path
            self.islink = os.path.islink(path)
            self.size = os.path.getsize(self.path) / 1024000
            self.age = int(time.strftime("%d", time.gmtime(time.time() - os.path.getmtime(self.path))))
            self.basename = os.path.basename(self.path)
            self.extension = os.path.splitext(self.path)[1]
            self.to_copy = True
            self.to_delete = False
        except:
            # erases all properties
            self.path = ""
            self.islink = False
            self.size = 0.0
            self.age = 0
            self.basename = ""
            self.extension = ""
            self.to_copy = False
            self.to_delete = False


    # copies the file to the destination
    def copy(self, destination):
        # if the file was marked and its not empty
        if self.to_copy and (not self.path == ""):
            # tries to copy the file
            try:
                # creates the receiving folder if doesnt exist yet
                if not os.path.isdir(destination):
                    os.makedirs(destination)

                # copies the file to destination
                shutil.copy(self.path, destination)
                # if the copy was done, return success
                return True
            # if something went wrong
            except:
                # returns error
                return False

        return True


    # removes the file
    def delete(self):
        # if it was marked for removal and its not empty
        if self.to_delete and (not self.path == ""):
            # tries to remove the file
            try:
                # removes the file from self.path
                os.remove(self.path)

                # erases all properties
                self.path = ""
                self.islink = False
                self.size = 0.0
                self.age = 0
                self.basename = ""
                self.extension = ""

                # if all went OK, return success
                return True
            # if something went wrong
            except:
                # returns error
                return False

        return True


    # returns if this file is a "filetype"
    def evaluate(self, filetype):
        # map with the evaluation and its test
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

        # splits the conditions on ;
        conditions = filetype.split(";")

        # tries to run the evaluation test for this file
        try:
            # for every condition identified
            for c in conditions:
                # if some evaluation returns true (; = or)
                if evaluations.get(c)():
                    # validates the file for the given conditions
                    return True

            # if no condition was validated, returns false
            return False
        # if the condition was not identified
        except:
            # returns false
            return False



class Tag:
    # creates a tag object containing some information
    def __init__(self, path):
        # tries to read information from the file
        try:
            self.file = eyed3.load(path)
            self.artist = self.file.tag.artist
            self.album = self.file.tag.album
            self.title = self.file.tag.title
            self.rating = math.ceil(self.file.tag.frame_set[b'POPM'][0].rating / 51)
        # if something went wrong
        except:
            self.artist = "<none>"
            self.album = "<none>"
            self.title = "<none>"
            self.rating = 0