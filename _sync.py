'''

This controls the sync and its options
Also implements every action related to a sync

'''


import _file
import _defaults
import _validations

import os
import ast
import json
import random


class Sync:
    def __init__(self, path):
        self.path = path # stores the path of the sync file (that is also its name in the schedule file)

    def load(self, log): # loads the sync from its path and validates its values
        try:
            log.report("ok_sync_running", detail=self.path)
            self.properties = json.loads(open(self.path, "r").read())
        except:
            log.report("error_sync_opening")
            return False

        if not self.validate_enable(self.properties, log):
            return False

        if not self.validate_source_path(self.properties, log):
            return False

        if not self.validate_source_selection_condition(self.properties, log):
            return False

        if not self.validate_source_maximum_age(self.properties, log):
            return False

        if not self.validate_source_subfolder_search(self.properties, log):
            return False

        if not self.validate_source_filelist_shuffle(self.properties, log):
            return False

        if not self.validate_destination_path(self.properties, log):
            return False

        if not self.validate_destination_selection_condition(self.properties, log):
            return False

        if not self.validate_destination_maximum_age(self.properties, log):
            return False

        if not self.validate_destination_subfolder_search(self.properties, log):
            return False

        if not self.validate_destination_filelist_shuffle(self.properties, log):
            return False

        if not self.validate_hierarchy_maintenance(self.properties, log):
            return False

        if not self.validate_left_files_deletion(self.properties, log):
            return False

        if not self.validate_file_override(self.properties, log):
            return False

        if not self.validate_size_limit(self.properties, log):
            return False

        if not self.validate_sync_cooldown(self.properties, log):
            return False

        log.report("ok_sync_json_load")
        return True


    def run(self, control, log): # runs this sync if needed
        if (self.path not in control.properties) or (control.its_time(self.path)): # will run if this sync is not scheduled or if its cooldown has ended
            if not ast.literal_eval(self.properties["enable"]): # checks if it is disabled before start running
                log.report("ok_sync_run_disabled")
                return True

            # creates a list of files inside the source folder
            source = File_List(
                self.properties["source_path"],
                self.properties["source_selection_condition"],
                self.properties["source_maximum_age"],
                ast.literal_eval(self.properties["source_subfolder_search"]),
                ast.literal_eval(self.properties["source_filelist_shuffle"])
            )

            # creates a list of files inside the destination folder
            destination = File_List(
                self.properties["destination_path"],
                self.properties["destination_selection_condition"],
                self.properties["destination_maximum_age"],
                ast.literal_eval(self.properties["destination_subfolder_search"]),
                ast.literal_eval(self.properties["destination_filelist_shuffle"])
            )


            if not source.fill(int(self.properties["size_limit"]), log): # fills the source file list with the specified size limit
                return False

            if not destination.fill(0, log): # fills the destination file list with no size limit
                return False

            if ast.literal_eval(self.properties["left_files_deletion"]):
                if not destination.mark_files_to_delete_except_by(source, ast.literal_eval(self.properties["hierarchy_maintenance"]), log): # marks files in the file list to be removed
                    return False

                if not destination.remove_marked_files(log): # removes the previously marked files
                    return False

                if not destination.remove_empty_folders(log): # removes empty folders in the destination
                    return False

            if not ast.literal_eval(self.properties["file_override"]):
                if not source.mark_files_to_copy_except_by(destination, ast.literal_eval(self.properties["hierarchy_maintenance"]), log): # unmarks redundant files to prevent overwriting
                    return False

            if not source.copy_marked_files(self.properties["destination_path"], ast.literal_eval(self.properties["hierarchy_maintenance"]), log): # copies the marked files
                return False

            control.schedule(self.path, int(self.properties["sync_cooldown"])) # schedules the next time to run this sync again
            log.report("ok_sync_finished")
            return True
        else:
            log.report("ok_sync_still_in_cooldown")
            return True

    def disable(self, log): # disables this sync (useful if an error occurred)
        try:
            self.properties["enable"] = "False"

            with open(self.path, "w") as file_to_write:
                json.dump(self.properties, file_to_write, indent=4, ensure_ascii=False)
                log.report("ok_sync_disable")
                return True
        except:
            log.report("error_sync_disable", critical=True)
            return False

    def validate_enable(self, json, log):
        if not "enable" in json:
            log.report("error_sync_enable_missing") # has to be specified
            return False

        if not _validations.validate_boolean_value(json["enable"]):
            log.report("error_sync_enable")
            return False

        return True

    def validate_source_path(self, json, log):
        if not "source_path" in json:
            log.report("error_sync_source_path_missing") # has to be specified
            return False

        if not _validations.validate_path(json["source_path"]):
            log.report("error_sync_source_path")
            return False

        return True

    def validate_source_selection_condition(self, json, log):
        if not "source_selection_condition" in json:
            json["source_selection_condition"] = _defaults.default_source_selection_condition # if wasn't found in the json, use the default value

        if not _validations.validate_selection_condition(json["source_selection_condition"]):
            log.report("error_sync_source_selection_condition")
            return False

        return True

    def validate_source_maximum_age(self, json, log):
        if not "source_maximum_age" in json:
            json["source_maximum_age"] = _defaults.default_source_maximum_age # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_zero(json["source_maximum_age"]):
            if not json["source_maximum_age"] == "any age":
                log.report("error_sync_source_maximum_age")
                return False

        return True

    def validate_source_subfolder_search(self, json, log):
        if not "source_subfolder_search" in json:
            json["source_subfolder_search"] = _defaults.default_source_subfolder_search # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["source_subfolder_search"]):
            log.report("error_sync_source_subfolder_search")
            return False

        return True

    def validate_source_filelist_shuffle(self, json, log):
        if not "source_filelist_shuffle" in json:
            json["source_filelist_shuffle"] = _defaults.default_source_filelist_shuffle # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["source_filelist_shuffle"]):
            log.report("error_sync_source_filelist_shuffle")
            return False

        return True

    def validate_destination_path(self, json, log):
        if not "destination_path" in json:
            log.report("error_sync_destination_path_missing") # has to be specified
            return False

        if not _validations.validate_path(json["destination_path"]):
            log.report("error_sync_destination_path")
            return False

        return True

    def validate_destination_selection_condition(self, json, log):
        if not "destination_selection_condition" in json:
            json["destination_selection_condition"] = _defaults.default_destination_selection_condition # if wasn't found in the json, use the default value

        if not _validations.validate_selection_condition(json["destination_selection_condition"]):
            log.report("error_sync_destination_selection_condition")
            return False

        return True

    def validate_destination_maximum_age(self, json, log):
        if not "destination_maximum_age" in json:
            json["destination_maximum_age"] = _defaults.default_destination_maximum_age # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_zero(json["destination_maximum_age"]):
            if not json["destination_maximum_age"] == "any age":
                log.report("error_sync_destination_maximum_age")
                return False

        return True

    def validate_destination_subfolder_search(self, json, log):
        if not "destination_subfolder_search" in json:
            json["destination_subfolder_search"] = _defaults.default_destination_subfolder_search # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["destination_subfolder_search"]):
            log.report("error_sync_destination_subfolder_search")
            return False

        return True

    def validate_destination_filelist_shuffle(self, json, log):
        if not "destination_filelist_shuffle" in json:
            json["destination_filelist_shuffle"] = _defaults.default_destination_filelist_shuffle # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["destination_filelist_shuffle"]):
            log.report("error_sync_destination_filelist_shuffle")
            return False

        return True

    def validate_hierarchy_maintenance(self, json, log):
        if not "hierarchy_maintenance" in json:
            json["hierarchy_maintenance"] = _defaults.default_hierarchy_maintenance # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["hierarchy_maintenance"]):
            log.report("error_sync_hierarchy_maintenance")
            return False

        return True

    def validate_left_files_deletion(self, json, log):
        if not "left_files_deletion" in json:
            json["left_files_deletion"] = _defaults.default_left_files_deletion # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["left_files_deletion"]):
            log.report("error_sync_left_files_deletion")
            return False

        return True

    def validate_file_override(self, json, log):
        if not "file_override" in json:
            json["file_override"] = _defaults.default_file_override # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["file_override"]):
            log.report("error_sync_file_override")
            return False

        return True

    def validate_size_limit(self, json, log):
        if not "size_limit" in json:
            json["size_limit"] = _defaults.default_size_limit # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_or_equal_to_zero(json["size_limit"]):
            log.report("error_sync_size_limit")
            return False

        return True

    def validate_sync_cooldown(self, json, log):
        if not "sync_cooldown" in json:
            json["sync_cooldown"] = _defaults.default_sync_cooldown # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_zero(json["sync_cooldown"]):
            log.report("error_sync_sync_cooldown")
            return False

        return True



class File_List: # creates a list of files
    def __init__(self, path, selection_condition, maximum_age, subfolder_search, filelist_shuffle):
        self.filelist = []
        self.path = path
        self.selection_condition = selection_condition
        self.maximum_age = maximum_age
        self.subfolder_search = subfolder_search
        self.filelist_shuffle = filelist_shuffle


    def fill(self, size_limit, log): # fills the file list
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            for f in filenames:
                file = _file.File(os.path.join(dirpath, f))

                if file.evaluate_type(self.selection_condition) and file.evaluate_age(self.maximum_age):
                    self.filelist.append(file)

            if not self.subfolder_search:
                break

        if self.filelist_shuffle: # will shuffle the file list if needed
            random.shuffle(self.filelist)

        if size_limit > 0: # will trim the file list to meet the specified limit
            total_size = 0.0

            for f in self.filelist:
                if total_size + f.size > size_limit:
                    self.filelist = self.filelist[:self.filelist.index(f)]
                    break
                else:
                    total_size += f.size

        log.report("ok_file_list_load", detail=self.path)
        return True


    def mark_files_to_delete_except_by(self, other, hierarchy_maintenance, log): # marks the leftover files to be removed
        for f_this in self.filelist:
            if not f_this.path == "":
                f_this.to_delete = True

                for f_other in other.filelist:
                    if not f_other.path == "":
                        if hierarchy_maintenance:
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                f_this.to_delete = False
                                break
                        elif f_this.path == os.path.join(self.path, f_other.basename):
                            f_this.to_delete = False
                            break

        log.report("ok_file_list_mark_files_to_delete")
        return True


    def mark_files_to_copy_except_by(self, other, hierarchy_maintenance, log): # unmarks redundant files to prevent being overwrited
        for f_this in self.filelist:
            f_this.to_copy = True

            if not f_this.path == "":
                for f_other in other.filelist:
                    if not f_other.path == "":
                        if hierarchy_maintenance:
                            if f_this.path.split(self.path, 1)[1] == f_other.path.split(other.path, 1)[1]:
                                f_this.to_copy = False
                                break
                        elif os.path.join(other.path, f_this.basename) == f_other.path:
                            f_this.to_copy = False
                            break

        log.report("ok_file_list_unmark_redundant_files")
        return True


    def remove_marked_files(self, log): # removes all marked files
        for f_this in self.filelist:
            if f_this.to_delete:
                if not f_this.delete(log):
                    log.report("error_file_list_remove_marked_files")
                    return False

        log.report("ok_file_list_remove_marked_files")
        return True


    def copy_marked_files(self, destination, hierarchy_maintenance, log): # copies all marked files to the destination folder
        for f_this in self.filelist:
            if f_this.to_copy:
                target_path = os.path.split(f_this.path.replace(self.path, destination))[0] if hierarchy_maintenance else destination

                if not f_this.copy(target_path, log):
                    log.report("error_file_list_copying_files")
                    return False

        log.report("ok_file_list_copying_files")
        return True


    def remove_empty_folders(self, log): # removes all empty folders under the path of this file list
        for (dirpath, dirnames, filenames) in os.walk(self.path, topdown=False):
            if dirpath == self.path:
                break

            else:
                if os.listdir(dirpath) == []:
                    try:
                        os.rmdir(dirpath)
                        log.report("ok_file_list_remove_empty_folder", detail=dirpath)
                    except:
                        log.report("error_file_list_remove_empty_folder", detail=dirpath)
                        log.report("error_file_list_remove_empty_folders")
                        return False

        log.report("ok_file_list_remove_empty_folders")
        return True