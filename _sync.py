import _log
import _file

import os
import ast
import random


class Sync:
    # creates a "sync" between two folders, given the parameters
    def __init__(self, source_path, source_selection_condition, source_subfolder_search, source_filelist_shuffle, destination_path, destination_selection_condition, destination_subfolder_search, destination_filelist_shuffle, hierarchy_maintenance, left_files_deletion, file_override, size_limit, log):
        # source path
        self.source_path = source_path
        # selection condition
        self.source_selection_condition = source_selection_condition
        # subfolder search toggle
        self.source_subfolder_search = ast.literal_eval(source_subfolder_search)
        # filelist shuffle toggle
        self.source_filelist_shuffle = ast.literal_eval(source_filelist_shuffle)

        # destination path
        self.destination_path = destination_path
        # selection condition
        self.destination_selection_condition = destination_selection_condition
        # subfolder search toggle
        self.destination_subfolder_search = ast.literal_eval(destination_subfolder_search)
        # filelist shuffle toggle
        self.destination_filelist_shuffle = ast.literal_eval(destination_filelist_shuffle)

        # directory hierarchy maintenance
        self.hierarchy_maintenance = ast.literal_eval(hierarchy_maintenance)
        # left files deletion toggle
        self.left_files_deletion = ast.literal_eval(left_files_deletion)
        # file override toggle
        self.file_override = ast.literal_eval(file_override)
        # size limit
        self.size_limit = int(size_limit)

        # log to report to
        self.log = log


    def run(self):
        # file list inits
        source = File_List(self.source_path, self.source_selection_condition, self.source_subfolder_search, self.source_filelist_shuffle, self.log)
        destination = File_List(self.destination_path, self.destination_selection_condition, self.destination_subfolder_search ,self.destination_filelist_shuffle, self.log)
        self.log.report("[ OK  ] file list initialize")

        # fill file lists
        source.fill(self.size_limit)
        destination.fill(0)
        self.log.report("[ OK  ] file list fill")

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
    def __init__(self, path, selection_condition, subfolder_search, filelist_shuffle, log):
        # file list
        self.filelist = []
        # path of the folder
        self.path = path
        # selection condition
        self.selection_condition = selection_condition
        # subflder search toggle
        self.subfolder_search = subfolder_search
        # filelist shuffle toggle
        self.filelist_shuffle = filelist_shuffle
        # log to report to
        self.log = log


    # fills self.filelist until size_limit with files that pass self.selection_condition
    def fill(self, size_limit):
        # walks in the directory
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            # for any file inside it
            for f in filenames:
                # creates a file object containing some information
                file = _file.File(dirpath + "/" + f)

                # if the file meets self.selection_condition
                if file.evaluate(self.selection_condition):
                    # include it in self.filelist
                    self.filelist.append(file)

            # if the subfolder search is disabled
            if not self.subfolder_search:
                # stops here (will stop at the first iteration)
                break

        # if filelist shuffle is enabled
        if self.filelist_shuffle:
            # shuffles self.filelist
            random.shuffle(self.filelist)

        # if size_limit was received (> 0)
        if size_limit > 0:
            total_size = 0.0
            i = 0

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
            # if its not empty
            if not f_this.path == "":
                # suppose it has to be removed
                f_this.to_delete = True

                # for any file in the other filelist
                for f_other in other.filelist:
                    # if its not empty
                    if not f_other.path == "":
                        # if hierarchy_maintenance was received
                        if hierarchy_maintenance:
                            # if both relative paths match
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                # the file does not have to be deleted
                                f_this.to_delete = False
                                break

                        # if the other file is the counterpart of this file
                        elif f_this.path == self.path + "/" + f_other.basename:
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
                    # if its not empty
                    if not f_other.path == "":
                        # if hierarchy_maintenance was received
                        if hierarchy_maintenance:
                            # if the relative paths match
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                # this file does not need to be copied
                                f_this.to_copy = False
                                break
                        # otherwise
                        else:
                            # if the other file is the counterpart of this file
                            if other.path + "/" + f_this.basename == f_other.path:
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
                    if f_this.copy(destination + f_this.path.split(self.path, 1)[1].rsplit(f_this.basename, 1)[0]):
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
            # if not
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