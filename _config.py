'''

This controls the configuration file and its options
Also implements every action related to that file

'''


import _paths
import _defaults
import _validations

import os
import ast
import json
import time
import subprocess


class Config:
    def __init__(self, root):
        self.path = os.path.join(root, _paths.config_folder, _paths.config_file) # stores the path to the configuration file

    def load(self, log): # loads the configuration file and validates its values
        try:
            self.properties = json.loads(open(self.path, "r").read())
        except:
            log.report("error_config_opening", critical=True)
            return False

        if not self.validate_check_cooldown(self.properties, log):
            return False

        if not self.validate_startup_delay(self.properties, log):
            return False

        if not self.validate_save_log(self.properties, log):
            return False

        if not self.validate_log_only_if_an_error_occur(self.properties, log):
            return False

        if not self.validate_logs_folder_maximum_size(self.properties, log):
            return False

        if self.validate_send_email(self.properties, log):
            if not self.validate_email_only_if_an_error_occur(self.properties, log):
                return False

            if not self.validate_email_sender(self.properties, log):
                return False

            if not self.validate_email_sender_password(self.properties, log):
                return False

            if not self.validate_email_addressee(self.properties, log):
                return False
        else:
            return False

        if not self.validate_post_sync_script(self.properties, log):
            return False


        log.report("ok_config_json_load")
        return True


    def validate_check_cooldown(self, json, log):
        if not "check_cooldown" in json:
            json["check_cooldown"] = _defaults.default_check_cooldown # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_zero(json["check_cooldown"]):
            log.report("error_config_check_cooldown", critical=True)
            return False

        return True

    def validate_startup_delay(self, json, log):
        if not "startup_delay" in json:
            json["startup_delay"] = _defaults.default_startup_delay # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_or_equal_to_zero(json["startup_delay"]):
            log.report("error_config_startup_delay", critical=True)
            return False

        return True

    def validate_save_log(self, json, log):
        if not "save_log" in json:
            json["save_log"] = _defaults.default_save_log # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["save_log"]):
            log.report("error_config_save_log", critical=True) # will return error if the value is invalid
            return False

        return True

    def validate_log_only_if_an_error_occur(self, json, log):
        if not "log_only_if_an_error_occur" in json:
            json["log_only_if_an_error_occur"] = _defaults.default_log_only_if_an_error_occur # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["log_only_if_an_error_occur"]):
            log.report("error_config_log_only_if_an_error_occur", critical=True) # will return error if the value is invalid
            return False

        return True


    def validate_logs_folder_maximum_size(self, json, log):
        if not "logs_folder_maximum_size" in json:
            json["logs_folder_maximum_size"] = _defaults.default_logs_folder_maximum_size # if wasn't found in the json, use the default value

        if not _validations.validate_integer_greater_than_or_equal_to_zero(json["logs_folder_maximum_size"]):
            log.report("error_config_logs_folder_maximum_size", critical=True) # will return error if the value is invalid
            return False

        return True

    def validate_send_email(self, json, log):
        if not "send_email" in json:
            json["send_email"] = _defaults.default_send_email # if wasn't found in the json, use the default value

        if not _validations.validate_boolean_value(json["send_email"]):
            log.report("error_config_send_email", critical=True) # will return error if the value is invalid
            return False

        return True

    def validate_email_only_if_an_error_occur(self, json, log):
        if not "email_only_if_an_error_occur" in json:
            log.report("error_config_email_only_if_an_error_occur_missing", critical=True) # has to be specified
            return False

        if not _validations.validate_boolean_value(json["email_only_if_an_error_occur"]):
            log.report("error_config_email_only_if_an_error_occur", critical=True) # will return error if the value is invalid
            return False

        return True

    def validate_email_sender(self, json, log):
        if not "email_sender" in json:
            log.report("error_config_email_sender_missing", critical=True) # has to be specified
            return False

        # no value validation applied
        return True

    def validate_email_sender_password(self, json, log):
        if not "email_sender_password" in json:
            log.report("error_config_email_sender_password_missing", critical=True) # has to be specified
            return False

        # no value validation applied
        return True

    def validate_email_addressee(self, json, log):
        if not "email_addressee" in json:
            log.report("error_config_email_addressee_missing", critical=True) # has to be specified
            return False

        # no value validation applied
        return True

    def validate_post_sync_script(self, json, log):
        if not "post_sync_script" in json:
            json["post_sync_script"] = _defaults.default_post_sync_script # if wasn't found in the json, use the default value

        # no value validation applied
        return True


    def run_startup_delay(self, log): # sleeps the specified startup delay
        time.sleep(int(self.properties["startup_delay"]) * 60)
        log.report("ok_config_startup_delay")
        return True

    def run_post_sync_script(self, log): # runs the post sync script
        if "post_sync_script" in self.properties:
            post_sync_script_subprocess = subprocess.Popen(self.properties["post_sync_script"], stdout=subprocess.PIPE, shell=True)
            (post_sync_script_output, error_code) = post_sync_script_subprocess.communicate()

            log.report("ok_config_post_sync_script_output", detail=self.properties["post_sync_script"])
            log.report(post_sync_script_output.decode()) # writes the console output in the log file
            log.report("ok_config_post_sync_script")

        return True

    def send_email(self, email, log): # sends the email if needed
        if ast.literal_eval(self.properties["send_email"]):
            if (ast.literal_eval(self.properties["email_only_if_an_error_occur"]) and log.error_occurred) or (not ast.literal_eval(self.properties["email_only_if_an_error_occur"])):
                email.send(self.properties["email_sender"], self.properties["email_sender_password"], self.properties["email_addressee"], log)
                # maybe pass out the email send return value
        return True

    def save_log(self, log): # writes the log file
        if ast.literal_eval(self.properties["save_log"]):
            if (ast.literal_eval(self.properties["log_only_if_an_error_occur"]) and log.error_occurred) or (not ast.literal_eval(self.properties["log_only_if_an_error_occur"])):
                return log.write()

    def run_logs_folder_maximum_size(self, root): # deletes old log files to meet the specified maximum folder size
        def get_folder_size(path):
            size = 0
            for (dirpath, dirnames, filenames) in os.walk(path):
                for f in filenames:
                    size += os.path.getsize(os.path.join(dirpath, f)) / 1024000
            return size

        path = os.path.join(root, _paths.logs_folder)

        try:
            if "logs_folder_maximum_size" in self.properties:
                if int(self.properties["logs_folder_maximum_size"]) > 0:
                    files = sorted(os.listdir(path), key=lambda x: os.stat(os.path.join(path, x)).st_mtime) # sorts the files by modified date
                    for f in files:
                        if get_folder_size(path) > int(self.properties["logs_folder_maximum_size"]):
                            if os.path.isfile(os.path.join(path, f)):
                                os.remove(os.path.join(path, f))
            return True
        except:
            return False


    def run_check_cooldown(self): # sleeps the program the specified amount of time
        time.sleep(int(self.properties["check_cooldown"]) * 60 * 60)
