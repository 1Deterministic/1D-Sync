'''

This stores all strings used by the program and associates them to an identifier
Will be useful to deal with localisation

'''

english = {
    "prefix_ok": "[ OK  ] ",
    "prefix_error": "[ERROR] ",
    "prefix_warning": "[WARN.] ",
    "prefix_spacing": "        ",
    "prefix_timestamp_spacing": "          ",

    # email
    "email_subject": "1D-Sync Alert Service",
    "email_header": "Last sync run status\n\n",

    # Config
    "ok_config_json_load": "config .json loaded",
    "ok_config_startup_delay": "waited the startup delay: ",
    "ok_config_post_sync_script_output": "post sync script output: ",
    "ok_config_post_sync_script": "post sync script executed: ",
    "error_config_opening": "could not read the config file, syntax error or missing file",
    "error_config_check_cooldown": "\tcheck_cooldown has an invalid value: ",
    "error_config_startup_delay": "\tstartup_delay has an invalid value: ",
    "error_config_save_log": "\tsave_log has an invalid value: ",
    "error_config_skip_log_if_nothing_happened": "\tskip_log_if_nothing_happened has an invalid value: ",
    "error_config_skip_log_on_success": "\tconfig_skip_log_on_success has an invalid value: ",
    "error_config_logs_folder_maximum_size": "\tlogs_folder_maximum_size has an invalid value: ",
    "error_config_send_email": "\tsend_email has an invalid value: ",
    "error_config_email_only_if_an_error_occur_missing": "\temail_only_if_an_error_occur not in .json when send_email is True",
    "error_config_email_only_if_an_error_occur": "\temail_only_if_an_error_occur has an invalid value: ",
    "error_config_email_sender_missing": "\temail_sender not in .json when send_email is True",
    "error_config_email_sender_password_missing": "\temail_sender_password not in .json when send_email is True",
    "error_config_email_addressee_missing": "\temail_addressee not in .json when send_email is True",
    "error_config_run_post_sync_script_only_if_a_sync_occur": "\trun_post_sync_script_only_if_a_sync_occur has an invalid value: ",
    "error_config_run_continuously": "\trun_continuously has an invalid value: ",

    # Control
    "ok_control_json_load": "control .json loaded",
    "ok_control_write": "control file updated, syncs scheduled",
    "error_control_opening": "could not read the control file, syntax error or missing file",
    "error_control_write": "could not write the config file",

    # Email
    "ok_email_send": "email sent to: ",
    "error_email_send": "email was not sent to: ",

    # Sync
    "ok_sync_json_load": "sync .json loaded",
    "ok_sync_running": "running sync: ",
    "ok_sync_still_in_cooldown": "did not run, still in cooldown",
    "ok_sync_run_disabled": "this sync is disabled in the .json",
    "ok_sync_disable": "this sync was disabled",
    "ok_sync_finished": "sync complete!",
    "error_sync_opening": "could not read the sync file, probably syntax error: ",
    "error_sync_enable_missing": "\tenable missing",
    "error_sync_enable": "\tenable has an invalid value: ",
    "error_sync_source_path": "\tsource_path has an invalid value: ",
    "error_sync_source_path_missing": "\tsource_path missing",
    "error_sync_source_selection_condition": "\tsource_selection_condition has an invalid value: ",
    "error_sync_source_subfolder_search": "\tsource_subfolder_search has an invalid value: ",
    "error_sync_source_filelist_shuffle": "\tsource_filelist_shuffle has an invalid value: ",
    "error_sync_source_subfolder_of_destination": "\t source folder is the same or a subdirectory of the destination folder",
    "error_sync_destination_subfolder_of_source": "\t destination folder is the same or a subdirectory of the source folder",
    "error_sync_destination_path": "\tdestination_path has an invalid value: ",
    "error_sync_destination_path_missing": "\tdestination_path missing",
    "error_sync_destination_selection_condition": "\tdestination_selection_condition has an invalid value: ",
    "error_sync_destination_subfolder_search": "\tdestination_subfolder_search has an invalid value: ",
    "error_sync_destination_filelist_shuffle": "\tdestination_filelist_shuffle has an invalid value: ",
    "error_sync_hierarchy_maintenance": "\thierarchy_maintenance has an invalid value: ",
    "error_sync_left_files_deletion": "\tleft_files_deletion has an invalid value: ",
    "error_sync_file_override": "\tfile_override has an invalid value: ",
    "error_sync_size_limit": "\tsize_limit has an invalid value: ",
    "error_sync_sync_cooldown": "\tsync_cooldown has an invalid value: ",
    "error_sync_disable": "could not disable the sync, stopping the execution",

    # File_List
    "ok_file_list_load": "file list loaded",
    "ok_file_list_mark_files_to_delete": "leftover files identified",
    "ok_file_list_remove_marked_files": "leftover files removed",
    "ok_file_list_remove_empty_folders": "empty folders removed",
    "ok_file_list_copying_files": "files copied",
    "ok_file_list_unmark_redundant_files": "redundant files unmarked",
    "ok_file_list_remove_empty_folder": "\tdeleted empty folder: ",
    "error_file_list_remove_marked_files": "removing leftover files",
    "error_file_list_remove_empty_folders": "removing empty folders",
    "error_file_list_copying_files": "copying files",
    "error_file_list_remove_empty_folder": "\tcould not delete empty folder: ",

    # File
    "ok_file_copy": "\tcopied file: ",
    "ok_file_delete": "\tdeleted file: ",
    "error_file_copy": "\tcould not copy file: ",
    "error_file_delete": "\tcould not delete file: ",
    "warning_selection_condition_operand_not_identified": "\tselection condition not identified: ",
    "warning_selection_condition_operand": "\tselection condition invalid value: ",

    "warning_file_evaluate_no_reference_value": "\tselection condition with no reference value: ",
    "warning_file_evaluate_eyed3_load": "\teyeD3 didn't load the file: ",
    "warning_file_evaluate_no_mathematical_comparsion": "\tselection condition with no mathematical comparsion: ",
    "warning_file_evaluate_mathematical_comparsion_not_identified": "\tmathematical comparsion not identified: ",

    # Log
    "message_repeated_lines": "        \tthe previous line was repeated this more times: "
}

languages = {
    "english": english
}

strings = languages["english"]