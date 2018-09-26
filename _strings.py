'''

This stores all strings used by the program and associates them to an identifier
Will be useful to deal with localisation

'''

english = {
    # email
    "email_subject": "1D-Sync Alert Service",
    "email_header": "Last sync run status\n\n",

    # Config
    "ok_config_json_load": "[ OK  ] config .json loaded",
    "ok_config_startup_delay": "[ OK  ] waited the startup delay",
    "ok_config_post_sync_script_output": "[ OK  ] post sync script output: ",
    "ok_config_post_sync_script": "[ OK  ] post sync script executed",
    "error_config_opening": "[ERROR] could not read the config file, syntax error of missing file",
    "error_config_check_cooldown": "[ERROR] \tcheck_cooldown: invalid value",
    "error_config_startup_delay": "[ERROR] \tstartup_delay: invalid value",
    "error_config_save_log": "[ERROR] \tsave_log: invalid value",
    "error_config_log_only_if_an_error_occur": "[ERROR] \tlog_only_if_an_error_occur: invalid value",
    "error_config_log_only_if_a_sync_occur": "[ERROR] \tlog_only_if_a_sync_occur: invalid value",
    "error_config_logs_folder_maximum_size": "[ERROR] \tlogs_folder_maximum_size: invalid value",
    "error_config_send_email": "[ERROR] \tsend_email: invalid value",
    "error_config_email_only_if_an_error_occur_missing": "[ERROR] \temail_only_if_an_error_occur not in .json when send_email is True",
    "error_config_email_only_if_an_error_occur": "[ERROR] \temail_only_if_an_error_occur: invalid value",
    "error_config_email_sender_missing": "[ERROR] \temail_sender not in .json when send_email is True",
    "error_config_email_sender_password_missing": "[ERROR] \temail_sender_password not in .json when send_email is True",
    "error_config_email_addressee_missing": "[ERROR] \temail_addressee not in .json when send_email is True",

    # Control
    "ok_control_json_load": "[ OK  ] control .json loaded",
    "ok_control_write": "[ OK  ] control file updated, syncs scheduled",
    "error_control_opening": "[ERROR] could not read the control file, syntax error of missing file",
    "error_control_write": "[ERROR] could not write the config file",

    # Email
    "ok_email_send": "[ OK  ] email sent",
    "error_email_send": "[ERROR] email was not sent",

    # Sync
    "ok_sync_json_load": "[ OK  ] sync .json loaded",
    "ok_sync_running": "[ OK  ] running sync: ",
    "ok_sync_still_in_cooldown": "[ OK  ] did not run, still in cooldown\n",
    "ok_sync_run_disabled": "[ OK  ] this sync is disabled in the .json\n",
    "ok_sync_disable": "[ OK  ] this sync was disabled\n",
    "ok_sync_finished": "[ OK  ] sync complete!\n",
    "error_sync_opening": "[ERROR] could not read the sync file, probably syntax error",
    "error_sync_enable_missing": "[ERROR] \tenable missing",
    "error_sync_enable": "[ERROR] \tenable: invalid value",
    "error_sync_source_path": "[ERROR] \tsource_path: invalid value",
    "error_sync_source_path_missing": "[ERROR] \tsource_path missing",
    "error_sync_source_selection_condition": "[ERROR] \tsource_selection_condition: invalid value",
    "error_sync_source_maximum_age": "[ERROR] \tsource_maximum_age: invalid value",
    "error_sync_source_subfolder_search": "[ERROR] \tsource_subfolder_search: invalid value",
    "error_sync_source_filelist_shuffle": "[ERROR] \tsource_filelist_shuffle: invalid value",
    "error_sync_source_subfolder_of_destination": "[ERROR] \t source folder is the same or a subdirectory of the destination folder",
    "error_sync_destination_subfolder_of_source": "[ERROR] \t destination folder is the same or a subdirectory of the source folder",
    "error_sync_destination_path": "[ERROR] \tdestination_path: invalid value",
    "error_sync_destination_path_missing": "[ERROR] \tdestination_path missing",
    "error_sync_destination_selection_condition": "[ERROR] \tdestination_selection_condition: invalid value",
    "error_sync_destination_maximum_age": "[ERROR] \tdestination_maximum_age: invalid value",
    "error_sync_destination_subfolder_search": "[ERROR] \tdestination_subfolder_search: invalid value",
    "error_sync_destination_filelist_shuffle": "[ERROR] \tdestination_filelist_shuffle: invalid value",
    "error_sync_hierarchy_maintenance": "[ERROR] \thierarchy_maintenance: invalid value",
    "error_sync_left_files_deletion": "[ERROR] \tleft_files_deletion: invalid value",
    "error_sync_file_override": "[ERROR] \tfile_override: invalid value",
    "error_sync_size_limit": "[ERROR] \tsize_limit: invalid value",
    "error_sync_sync_cooldown": "[ERROR] \tsync_cooldown: invalid value",
    "error_sync_disable": "[ERROR] could not disable the sync, stopping the execution\n",

    # File_List
    "ok_file_list_load": "[ OK  ] file list loaded: ",
    "ok_file_list_mark_files_to_delete": "[ OK  ] leftover files identified",
    "ok_file_list_remove_marked_files": "[ OK  ] leftover files removed",
    "ok_file_list_remove_empty_folders": "[ OK  ] empty folders removed",
    "ok_file_list_copying_files": "[ OK  ] files copied",
    "ok_file_list_unmark_redundant_files": "[ OK  ] redundant files unmarked",
    "ok_file_list_remove_empty_folder": "[ OK  ] \tdeleted empty folder: ",
    "error_file_list_remove_marked_files": "[ERROR] removing leftover files",
    "error_file_list_remove_empty_folders": "[ERROR] removing empty folders",
    "error_file_list_copying_files": "[ERROR] copying files",
    "error_file_list_remove_empty_folder": "[ERROR] \tcould not delete empty folder: ",

    # File
    "ok_file_copy": "[ OK  ] \tcopied file: ",
    "ok_file_delete": "[ OK  ] \tdeleted file: ",
    "error_file_copy": "[ERROR] \tcould not copy file: ",
    "error_file_delete": "[ERROR] \tcould not delete file: "
}

languages = {
    "english": english
}

strings = languages["english"]