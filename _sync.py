import _file

import os
import ast
import random


class Sync:
    # creates a "sync" from the source folder to the destination folder
    def __init__(self, source_path, source_selection_condition, source_maximum_age, source_subfolder_search, source_filelist_shuffle,
                destination_path, destination_selection_condition, destination_maximum_age, destination_subfolder_search, destination_filelist_shuffle,
                 hierarchy_maintenance, left_files_deletion, file_override, size_limit, log):

        # source parameters
        self.source_path = source_path
        self.source_selection_condition = source_selection_condition
        self.source_maximum_age = source_maximum_age
        self.source_subfolder_search = ast.literal_eval(source_subfolder_search)
        self.source_filelist_shuffle = ast.literal_eval(source_filelist_shuffle)

        # destination parameters
        self.destination_path = destination_path
        self.destination_selection_condition = destination_selection_condition
        self.destination_maximum_age = destination_maximum_age
        self.destination_subfolder_search = ast.literal_eval(destination_subfolder_search)
        self.destination_filelist_shuffle = ast.literal_eval(destination_filelist_shuffle)

        # sync parameters
        self.hierarchy_maintenance = ast.literal_eval(hierarchy_maintenance)
        self.left_files_deletion = ast.literal_eval(left_files_deletion)
        self.file_override = ast.literal_eval(file_override)
        self.size_limit = int(size_limit)

        # log to report to
        self.log = log


    # performs an already initialized sync
    def run(self):
        # initializes the file lists
        source = File_List(self.source_path,
                           self.source_selection_condition,
                           self.source_maximum_age,
                           self.source_subfolder_search,
                           self.source_filelist_shuffle,
                           self.log)
        destination = File_List(self.destination_path,
                                self.destination_selection_condition,
                                self.destination_maximum_age,
                                self.destination_subfolder_search,
                                self.destination_filelist_shuffle,
                                self.log)
        self.log.report("[ OK  ] file list initialize")

        # fills the file lists
        source.fill(self.size_limit)
        destination.fill(0)
        self.log.report("[ OK  ] file list fill")

        # in case removing left files was received
        if self.left_files_deletion:
            # marks the files that will be removed
            destination.mark_files_to_delete_except_by(source, self.hierarchy_maintenance)
            self.log.report("[ OK  ] left files identification")

            # delete them
            if destination.remove_marked_files():
                self.log.report("[ OK  ] left files removal")
            else:
                self.log.report("[ERROR] left files removal")
                return False

            # after removing the files, also remove the empty folders
            if destination.remove_empty_folders():
                self.log.report("[ OK  ] empty folders removal")
            else:
                self.log.report("[ERROR] empty folders removal")
                return False

        # if the existing files will be maintained
        if not self.file_override:
            # unmarks the files that doesnt need to be copied
            source.mark_files_to_copy_except_by(destination, self.hierarchy_maintenance)
            self.log.report("[ OK  ] redundant files identification")

        # copies the marked files (all files are marked unless they were unmarked before)
        if source.copy_marked_files(self.destination_path, self.hierarchy_maintenance):
            self.log.report("[ OK  ] files copy")
        else:
            self.log.report("[ERROR] files copy")
            return False

        return True



class File_List:
    # creates a file list given the parameters
    def __init__(self, path, selection_condition, maximum_age, subfolder_search, filelist_shuffle, log):
        self.filelist = []
        self.path = path
        self.selection_condition = selection_condition
        self.maximum_age = maximum_age
        self.subfolder_search = subfolder_search
        self.filelist_shuffle = filelist_shuffle

        self.log = log


    # fills the list with files that pass the condition until the size limit is reached
    def fill(self, size_limit):
        # walks in the directory
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            # for any file inside it
            for f in filenames:
                # creates a file object containing some information
                file = _file.File(os.path.join(dirpath, f))

                # if the file meets the conditions
                if file.evaluate_type(self.selection_condition) and file.evaluate_age(self.maximum_age):
                    # include it in the list
                    self.filelist.append(file)

            # if the subfolder search is disabled
            if not self.subfolder_search:
                # stops here (will stop at the first iteration)
                break

        # if filelist shuffle is enabled
        if self.filelist_shuffle:
            random.shuffle(self.filelist)

        # if size_limit was received (> 0)
        if size_limit > 0:
            # total processed size
            total_size = 0.0

            # for every file in self.filelist
            for f in self.filelist:
                # if the total size including f exceeds size_limit
                if total_size + f.size > size_limit:
                    # cuts the file list here
                    self.filelist = self.filelist[:self.filelist.index(f)]
                    # breaks the loop
                    break
                # if doesnt exceed
                else:
                    # udates the size and goes to the next file
                    total_size += f.size

        # everything went OK, return success
        return True


    # marks the files that will be removed
    def mark_files_to_delete_except_by(self, other, hierarchy_maintenance):
        # for every file in this filelist
        for f_this in self.filelist:
            # if it's not empty
            if not f_this.path == "":
                # suppose it has to be removed
                f_this.to_delete = True

                # for any file in the other filelist
                for f_other in other.filelist:
                    # if it's not empty
                    if not f_other.path == "":
                        # if hierarchy_maintenance was received
                        if hierarchy_maintenance:
                            # if both relative paths match
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                # the file does not have to be deleted
                                f_this.to_delete = False
                                break
                        # if wasn't, check for the basename to be equal
                        elif f_this.path == os.path.join(self.path, f_other.basename):
                            # the file does not have to be deleted
                            f_this.to_delete = False
                            break

        return True


    # marks the files that will be copied (unmarks those who wont)
    def mark_files_to_copy_except_by(self, other, hierarchy_maintenance):
        # for every file in source list
        for f_this in self.filelist:
            # suppose it have to be copied
            f_this.to_copy = True

            # if its not empty
            if not f_this.path == "":
                # for every file in the other filelist
                for f_other in other.filelist:
                    # if it's not empty
                    if not f_other.path == "":
                        # if hierarchy_maintenance was received
                        if hierarchy_maintenance:
                            # if the relative paths match
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                # this file does not need to be copied
                                f_this.to_copy = False
                                break
                        # if wasn't, check for the basename to be equal
                        elif os.path.join(other.path, f_this.basename) == f_other.path:
                            # this file does not need to be copied
                            f_this.to_copy = False
                            break

        return True


    # removes the previously marked files
    def remove_marked_files(self):
        # for every file in filelist
        for f_this in self.filelist:
            if f_this.to_delete:
                filename = f_this.path
                # deletes the file
                if f_this.delete():
                    self.log.report("[ OK  ] \tdelete " + filename)
                else:
                    self.log.report("[ERROR] \tdelete " + filename)
                    return False

        return True


    # copies all marked files (will skip those unmarked)
    def copy_marked_files(self, destination, hierarchy_maintenance):
        # for every file in filelist
        for f_this in self.filelist:
            if f_this.to_copy:
                # if hierarchy_maintenance was received
                if hierarchy_maintenance:
                    # copies the file to its respective location under the destination root
                    if f_this.copy(os.path.split(f_this.path.replace(self.path, destination))[0]):
                        self.log.report("[ OK  ] \tcopy " + f_this.path)
                    else:
                        self.log.report("[ERROR] \tcopy " + f_this.path)
                        return False

                # otherwise
                else:
                    # copies the file to destination root folder
                    if f_this.copy(destination):
                        self.log.report("[ OK  ] \tcopy " + f_this.path)
                    else:
                        self.log.report("[ERROR] \tcopy " + f_this.path)
                        return False

        return True


    # removes all left empty folders in this folder
    def remove_empty_folders(self):
        # iterates the directory tree from the bottom
        for (dirpath, dirnames, filenames) in os.walk(self.path, topdown=False):
            # if the current dir is the root, stops
            if dirpath == self.path:
                break

            # if it isn't
            else:
                # if this dir is empty
                if os.listdir(dirpath) == []:
                    try:
                        # removes the folder
                        os.rmdir(dirpath)
                        self.log.report("[ OK  ] \tdelete " + dirpath + " folder")
                    except:
                        self.log.report("[ERROR] \tdelete " + dirpath + " folder")
                        return False

        return True