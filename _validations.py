import os

# returns if a loaded json sync is valid
def validate_sync_json(json, log):
    log.report("        checking the json file...")

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
    if not "source_selection_condition" in json:
        log.report("[ERROR] \t\"source_selection_condition\" not in .json")
        return False
    if not validate_selection_condition(json["source_selection_condition"]):
        log.report("[ERROR] \t\"source_selection_condition\": invalid value")
        return False

    # source_subfolder_search
    if not "source_subfolder_search" in json:
        log.report("[ERROR] \t\"source_subfolder_search\" not in .json")
        return False
    if not validate_toggle(json["source_subfolder_search"]):
        log.report("[ERROR] \t\"source_subfolder_search\": invalid value")
        return False

    # source_filelist_shuffle
    if not "source_filelist_shuffle" in json:
        log.report("[ERROR] \t\"source_filelist_shuffle\" not in .json")
        return False
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
    if not "destination_selection_condition" in json:
        log.report("[ERROR] \t\"destination_selection_condition\" not in .json")
        return False
    if not validate_selection_condition(json["destination_selection_condition"]):
        log.report("[ERROR] \t\"destination_selection_condition\": invalid value")
        return False

    # destination_subfolder_search
    if not "destination_subfolder_search" in json:
        log.report("[ERROR] \t\"destination_subfolder_search\" not in .json")
        return False
    if not validate_toggle(json["destination_subfolder_search"]):
        log.report("[ERROR] \t\"destination_subfolder_search\": invalid value")
        return False

    # destination_filelist_shuffle
    if not "destination_filelist_shuffle" in json:
        log.report("[ERROR] \t\"destination_filelist_shuffle\" not in .json")
        return False
    if not validate_toggle(json["destination_filelist_shuffle"]):
        log.report("[ERROR] \t\"destination_filelist_shuffle\": invalid value")
        return False

    # hierarchy_maintenance
    if not "hierarchy_maintenance" in json:
        log.report("[ERROR] \t\"hierarchy_maintenance\" not in .json")
        return False
    if not validate_toggle(json["hierarchy_maintenance"]):
        log.report("[ERROR] \t\"hierarchy_maintenance\": invalid value")
        return False

    # left_files_deletion
    if not "left_files_deletion" in json:
        log.report("[ERROR] \t\"left_files_deletion\" not in .json")
        return False
    if not validate_toggle(json["left_files_deletion"]):
        log.report("[ERROR] \t\"left_files_deletion\": invalid value")
        return False

    # file_override
    if not "file_override" in json:
        log.report("[ERROR] \t\"file_override\" not in .json")
        return False
    if not validate_toggle(json["file_override"]):
        log.report("[ERROR] \t\"file_override\": invalid value")
        return False

    # size_limit
    if not "size_limit" in json:
        log.report("[ERROR] \t\"size_limit\" not in .json")
        return False
    if not validate_size_limit(json["size_limit"]):
        log.report("[ERROR] \t\"size_limit\": invalid value")
        return False

    # sync_cooldown
    if not "sync_cooldown" in json:
        log.report("[ERROR] \t\"sync_cooldown\" not in .json")
        return False
    if not validate_sync_cooldown(json["sync_cooldown"]):
        log.report("[ERROR] \t\"sync_cooldown\": invalid value")
        return False

    return True


def validate_control_json(json, log):
    return True


def validate_config_json(json, log):
    # check_cooldown
    if not "check_cooldown" in json:
        log.report("[ERROR] \t\"check_cooldown\" not in .json")
        return False
    if not validate_config_cooldown(json["check_cooldown"]):
        log.report("[ERROR] \t\"check_cooldown\": invalid value")
        return False

    # email_sender
    if not "email_sender" in json:
        log.report("[ERROR] \t\"email_sender\" not in .json")
        return False

    # email_sender_password
    if not "email_sender_password" in json:
        log.report("[ERROR] \t\"email_sender_password\" not in .json")
        return False

    # email_addressee
    if not "email_addressee" in json:
        log.report("[ERROR] \t\"email_addressee\" not in .json")
        return False

    return True


# validates a path
def validate_path(path):
    return os.path.isdir(path)

# validates a selection condition
def validate_selection_condition(condition):
    return True

# validates a toggle
def validate_toggle(value):
    return value == "True" or value == "False"

# validates a size limit value
def validate_size_limit(value):
    try:
        value = int(value)

        if value >= 0:
            return True

        return False

    except:
        return False

# validates a cooldown value for a sync
def validate_sync_cooldown(cooldown):
    try:
        cooldown = int(cooldown)

        if cooldown > 0:
            return True
        else:
            return False

    except:
        return False

# validates a cooldown value for the main loop
def validate_config_cooldown(cooldown):
    try:
        cooldown = int(cooldown)

        if cooldown > 0:
            return True
        else:
            return False

    except:
        return False