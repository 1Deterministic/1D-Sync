import ast
import os

import _defaults

# returns if a loaded json sync is valid
def validate_sync_json(json, log):
    log.report("        checking the json file...")

    # defaults the optional values not found in the json file
    if not "source_selection_condition" in json: json["source_selection_condition"] = _defaults.default_source_selection_condition
    if not "source_maximum_age" in json: json["source_maximum_age"] = _defaults.default_source_maximum_age
    if not "source_subfolder_search" in json: json["source_subfolder_search"] = _defaults.default_source_subfolder_search
    if not "source_filelist_shuffle" in json: json["source_filelist_shuffle"] = _defaults.default_source_filelist_shuffle
    if not "destination_selection_condition" in json: json["destination_selection_condition"] = _defaults.default_destination_selection_condition
    if not "destination_maximum_age" in json: json["destination_maximum_age"] = _defaults.default_destination_maximum_age
    if not "destination_subfolder_search" in json: json["destination_subfolder_search"] = _defaults.default_destination_subfolder_search
    if not "destination_filelist_shuffle" in json: json["destination_filelist_shuffle"] = _defaults.default_destination_filelist_shuffle
    if not "hierarchy_maintenance" in json: json["hierarchy_maintenance"] = _defaults.default_hierarchy_maintenance
    if not "left_files_deletion" in json: json["left_files_deletion"] = _defaults.default_left_files_deletion
    if not "file_override" in json: json["file_override"] = _defaults.default_file_override
    if not "size_limit" in json: json["size_limit"] = _defaults.default_size_limit
    if not "sync_cooldown" in json: json["sync_cooldown"] = _defaults.default_sync_cooldown

    # enable
    if not "enable" in json:
        log.report("[ERROR] \t\"enable\" not in .json")
        return False
    if not validate_toggle(json["enable"]):
        log.report("[ERROR] \t\"enable\": invalid value")
        return False

    # source_path
    if not "source_path" in json:
        log.report("[ERROR] \t\"source_path\" not in .json")
        return False
    if not validate_path(json["source_path"]):
        log.report("[ERROR] \t\"source_path\": invalid path")
        return False

    # source_selection_condition
    if not validate_selection_condition(json["source_selection_condition"]):
        log.report("[ERROR] \t\"source_selection_condition\": invalid value")
        return False

    # source_maximum_age
    if not validate_maximum_age(json["source_maximum_age"]):
        log.report("[ERROR] \t\"source_maximum_age\": invalid value")
        return False

    # source_subfolder_search
    if not validate_toggle(json["source_subfolder_search"]):
        log.report("[ERROR] \t\"source_subfolder_search\": invalid value")
        return False

    # source_filelist_shuffle
    if not validate_toggle(json["source_filelist_shuffle"]):
        log.report("[ERROR] \t\"source_filelist_shuffle\": invalid value")
        return False

    # destination_path
    if not "destination_path" in json:
        log.report("[ERROR] \t\"destination_path\" not in .json")
        return False
    if not validate_path(json["destination_path"]):
        log.report("[ERROR] \t\"destination_path\": invalid value")
        return False

    # destination_selection_condition
    if not validate_selection_condition(json["destination_selection_condition"]):
        log.report("[ERROR] \t\"destination_selection_condition\": invalid value")
        return False

    # destination_maximum_age
    if not validate_maximum_age(json["destination_maximum_age"]):
        log.report("[ERROR] \t\"destination_maximum_age\": invalid value")
        return False

    # destination_subfolder_search
    if not validate_toggle(json["destination_subfolder_search"]):
        log.report("[ERROR] \t\"destination_subfolder_search\": invalid value")
        return False

    # destination_filelist_shuffle
    if not validate_toggle(json["destination_filelist_shuffle"]):
        log.report("[ERROR] \t\"destination_filelist_shuffle\": invalid value")
        return False

    # hierarchy_maintenance
    if not validate_toggle(json["hierarchy_maintenance"]):
        log.report("[ERROR] \t\"hierarchy_maintenance\": invalid value")
        return False

    # left_files_deletion
    if not validate_toggle(json["left_files_deletion"]):
        log.report("[ERROR] \t\"left_files_deletion\": invalid value")
        return False

    # file_override
    if not validate_toggle(json["file_override"]):
        log.report("[ERROR] \t\"file_override\": invalid value")
        return False

    # size_limit
    if not validate_size_limit(json["size_limit"]):
        log.report("[ERROR] \t\"size_limit\": invalid value")
        return False

    # sync_cooldown
    if not validate_sync_cooldown(json["sync_cooldown"]):
        log.report("[ERROR] \t\"sync_cooldown\": invalid value")
        return False

    return True


def validate_control_json(json, log):
    return True # CHECK IF ITS A VALID JSON


def validate_config_json(json, log):
    # defaults the optional values not found in the json file
    if not "check_cooldown" in json: json["check_cooldown"] = _defaults.default_check_cooldown
    if not "save_log" in json: json["save_log"] = _defaults.default_save_log
    if not "logs_folder_maximum_size" in json: json["logs_folder_maximum_size"] = _defaults.default_logs_folder_maximum_size
    if not "send_email" in json: json["send_email"] = _defaults.default_send_email
    if not "log_only_if_an_error_occur" in json: json["log_only_if_an_error_occur"] = _defaults.default_log_only_if_an_error_occur


    # check_cooldown
    if not validate_config_cooldown(json["check_cooldown"]):
        log.report("[ERROR] \t\"check_cooldown\": invalid value")
        return False

    # save_log
    if not validate_toggle(json["save_log"]):
        log.report("[ERROR] \t\"save_log\": invalid value")
        return False

    # log_only_if_an_error_occur
    if not validate_toggle(json["log_only_if_an_error_occur"]):
        log.report("[ERROR] \t\"log_only_if_an_error_occur\": invalid value")
        return False

    # logs_folder_maximum_size
    if not validate_size_limit(json["logs_folder_maximum_size"]):
            log.report("[ERROR] \t\"logs_folder_maximum_size\": invalid value")
            return False

    # send_email
    if not validate_toggle(json["send_email"]):
        log.report("[ERROR] \t\"send_email\": invalid value")
        return False
    elif ast.literal_eval(json["send_email"]):
        # options required when send_email is True

        # email_sender
        if not "email_sender" in json:
            log.report("[ERROR] \t\"email_sender\" not in .json when send_email is True")
            return False

        # email_sender_password
        if not "email_sender_password" in json:
            log.report("[ERROR] \t\"email_sender_password\" not in .json when send_email is True")
            return False

        # email_addressee
        if not "email_addressee" in json:
            log.report("[ERROR] \t\"email_addressee\" not in .json when send_email is True")
            return False

        # email_only_if_an_error_occur
        if not "email_only_if_an_error_occur" in json:
            log.report("[ERROR] \t\"email_only_if_an_error_occur\" not in .json when send_email is True")
            return False
        if not validate_toggle(json["email_only_if_an_error_occur"]):
            log.report("[ERROR] \t\"email_only_if_an_error_occur\": invalid value")
            return False

    # post_sync_script is now optional

    return True


# validates a path
def validate_path(path):
    return os.path.isdir(path)


# validates a selection condition
def validate_selection_condition(condition):
    # holds a list of supported selection conditions based on _filetypes lists
    supported_conditions= [
        # multimedia
        "audio",
        "image",
        "video",

        # office
        "document",
        "sheet",
        "presentation",

        # special cases
        "favorite audio",
        "any file",
        "none"
    ]

    # splits the conditions and checks them one by one
    conditions = condition.split(";")
    try:
        for c in conditions:
            if c in supported_conditions:
                continue
            else:
                return False
        return True
    except:
        return False


# validates an age condition
def validate_maximum_age(age):
    if age == "any age": return True
    else:
        try:
            return int(age) > 0
        except:
            return False


# validates a toggle
def validate_toggle(value):
    return value == "True" or value == "False"

# validates a size limit value
def validate_size_limit(value):
    try:
        return int(value) >= 0

    except:
        return False


# validates a cooldown value for a sync
def validate_sync_cooldown(cooldown):
    try:
        return int(cooldown) > 0

    except:
        return False


# validates a cooldown value for the main loop
def validate_config_cooldown(cooldown):
    try:
        return int(cooldown) > 0

    except:
        return False