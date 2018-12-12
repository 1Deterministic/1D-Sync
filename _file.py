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
        log = argument

        # some string split can fail
        try:
            # restore spaces
            actual_condition = condition.replace(_defaults.default_space_symbol_placeholder, " ")

            # ext
            if actual_condition.startswith(_defaults.default_ext_condition_chooser):
                reference_value = actual_condition.split(":", 1)[1]
                if reference_value == "":
                    log.report("warning_file_evaluate_no_reference_value", detail=condition)
                    return False

                return self.extension == actual_condition.split(":", 1)[1]

            # type
            elif actual_condition.startswith(_defaults.default_type_condition_chooser):
                reference_value = actual_condition.split(":", 1)[1]
                if reference_value == "":
                    log.report("warning_file_evaluate_no_reference_value", detail=condition)
                    return False

                return magic.Magic(mime=True).from_file(self.path).startswith(reference_value)

            # eyed3
            elif actual_condition.startswith(_defaults.default_eyed3_condition_chooser):
                tag = actual_condition.split(":", 1)[1]
                if tag == "":
                    log.report("warning_file_evaluate_no_reference_value", detail=condition)
                    return False

                if not self.tag.loaded:
                    # prevents trying to load incompatible files
                    # maybe improve to using MIME
                    if not self.extension == ".mp3":
                        return False

                    if not self.tag.load(self.path):
                        log.report("warning_file_evaluate_eyed3_load", detail=self.path)
                        return False


                if tag.startswith(_defaults.default_eyed3_tag_artist_chooser):
                    reference_value = tag.split(":", 1)[1]

                    if reference_value == "":
                        log.report("warning_file_evaluate_no_reference_value", detail=condition)
                        return False

                    return self.tag.artist == reference_value

                elif tag.startswith(_defaults.default_eyed3_tag_album_chooser):
                    reference_value = tag.split(":", 1)[1]
                    if reference_value == "":
                        log.report("warning_file_evaluate_no_reference_value", detail=condition)
                        return False

                    return self.tag.album == reference_value

                elif tag.startswith(_defaults.default_eyed3_tag_title_chooser):
                    reference_value = tag.split(":", 1)[1]
                    if reference_value == "":
                        log.report("warning_file_evaluate_no_reference_value", detail=condition)
                        return False

                    return self.tag.title == reference_value

                elif tag.startswith(_defaults.default_eyed3_tag_rating_chooser):
                    mathematical_comparsion = tag.split(":", 1)[1]
                    if mathematical_comparsion == "":
                        log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                        return False

                    comparsion = mathematical_comparsion.split(":", 1)[0]
                    if comparsion == "":
                        log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                        return False

                    reference_value = mathematical_comparsion.split(":", 1)[1]
                    if reference_value == "":
                        log.report("warning_file_evaluate_no_reference_value", detail=condition)
                        return False

                    return self.condition_compare_int(self.tag.rating, comparsion, reference_value, log)

                return False

            # age
            elif actual_condition.startswith(_defaults.default_age_condition_chooser):
                age = actual_condition.split(":", 1)[1]
                if age == "":
                    log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                    return False

                comparsion = age.split(":", 1)[0]
                if comparsion == "":
                    log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                    return False

                reference_value = age.split(":", 1)[1]
                if reference_value == "":
                    log.report("warning_file_evaluate_no_reference_value", detail=condition)
                    return False

                return self.condition_compare_int(self.age, comparsion, reference_value, log)

            # size
            elif actual_condition.startswith(_defaults.default_size_condition_chooser):
                size = actual_condition.split(":", 1)[1]
                if size == "":
                    log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                    return False

                comparsion = size.split(":", 1)[0]
                if comparsion == "":
                    log.report("warning_file_evaluate_no_mathematical_comparsion", detail=condition)
                    return False

                reference_value = size.split(":", 1)[1]
                if reference_value == "":
                    log.report("warning_file_evaluate_no_reference_value", detail=condition)
                    return False

                return self.condition_compare_int(self.size, comparsion, reference_value, log)

            # generic
            elif actual_condition == _defaults.default_anyfile_condition_chooser:
                return True

            elif actual_condition == _defaults.default_none_condition_chooser:
                return False

            # could not validate
            else:
                log.report("warning_selection_condition_operand_not_identified", detail=condition)
                return False

        except:
            log.report("warning_selection_condition_operand", detail=condition)
            return False

    # compares two values and return according to a received condition
    def condition_compare_int(self, value_a, comparsion, value_b, log):
        try:
            a = int(value_a)
            b = int(value_b)

            if comparsion == _defaults.default_math_compare_equal:
                return a == b
            if comparsion == _defaults.default_math_compare_different:
                return not a == b
            if comparsion == _defaults.default_math_compare_strictly_greater:
                return a > b
            if comparsion == _defaults.default_math_compare_strictly_lesser:
                return a < b
            if comparsion == _defaults.default_math_compare_greater_than_or_equal_to:
                return a >= b
            if comparsion == _defaults.default_math_compare_lesser_than_or_equal_to:
                return a <= b
            else:
                raise Exception
        except:
            log.report("warning_file_evaluate_mathematical_comparsion_not_identified", detail=comparsion+":"+value_b)
            return False


class Tag:
    def __init__(self):
        self.loaded = False

    def load(self, path):
        try:
            # a fail here will trigger a warning
            self.file = eyed3.load(path)

            try: self.title = self.file.tag.title
            except: self.title = "<none>"

            try: self.album = self.file.tag.album
            except: self.album = "<none>"

            try:self.artist = self.file.tag.artist
            except: self.artist = "<none>"

            # this frame set can be missing if the rating is unset
            try: self.rating = math.ceil(self.file.tag.frame_set[b'POPM'][0].rating / 51)
            except: self.rating = 0

            self.loaded = True
            return True
        except:
            return False
