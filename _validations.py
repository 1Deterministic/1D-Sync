import os

# returns if a loaded json sync is valid
def validate_sync_json(json):
    if not "enable" in json:
        return False
    if not validate_toggle(json["enable"]):
        return False

    if not "source_path" in json:
        return False
    if not validate_path(json["source_path"]):
        return False

    if not "source_selection_condition" in json:
        return False
    if not validate_selection_condition(json["source_selection_condition"]):
        return False

    if not "source_subfolder_search" in json:
        return False
    if not validate_toggle(json["source_subfolder_search"]):
        return False

    if not "source_filelist_shuffle" in json:
        return False
    if not validate_toggle(json["source_filelist_shuffle"]):
        return False

    if not "destination_path" in json:
        return False
    if not validate_path(json["destination_path"]):
        return False

    if not "destination_selection_condition" in json:
        return False
    if not validate_selection_condition(json["destination_selection_condition"]):
        return False

    if not "destination_subfolder_search" in json:
        return False
    if not validate_toggle(json["destination_subfolder_search"]):
        return False

    if not "destination_filelist_shuffle" in json:
        return False
    if not validate_toggle(json["destination_filelist_shuffle"]):
        return False

    if not "hierarchy_maintenance" in json:
        return False
    if not validate_toggle(json["hierarchy_maintenance"]):
        return False

    if not "left_files_deletion" in json:
        return False
    if not validate_toggle(json["left_files_deletion"]):
        return False

    if not "file_override" in json:
        return False
    if not validate_toggle(json["file_override"]):
        return False

    if not "size_limit" in json:
        return False
    if not validate_size_limit(json["size_limit"]):
        return False

    if not "sync_cooldown" in json:
        return False
    if not validate_sync_cooldown(json["sync_cooldown"]):
        return False

    return True


def validate_control_json(json):
    return True


def validate_config_json(json):
    if not "check_cooldown" in json:
        return False
    if not validate_config_cooldown(json["check_cooldown"]):
        return False

    if not "email_sender" in json:
        return False

    if not "email_sender_password" in json:
        return False

    if not "email_addressee" in json:
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

# validates a cooldown value
def validate_sync_cooldown(cooldown):
    try:
        values = cooldown.split("-")

        if len(values) == 2:
            values[0] = int(values[0])
            values[1] = int(values[1])

            if isinstance(values[0], int) and isinstance(values[1], int):
                if values[0] > 0 and values[1] > 0:
                    if values[1] >= values[0]:
                        return True

        return False

    except:
        return False


def validate_config_cooldown(cooldown):
    try:
        cooldown = int(cooldown)

        if cooldown > 0:
            return True
        else:
            return False

    except:
        return False