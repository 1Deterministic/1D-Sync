import _log
import _sync
import _validations
import _email
import _about

import os
import ast
import subprocess
import json
import time
import datetime
import logging


if __name__ == "__main__":
    # hides eyed3 logs on terminal
    logging.getLogger("eyed3").setLevel(logging.CRITICAL)

    # stores the path of the current directory
    this_path = os.path.dirname(os.path.realpath(__file__))

    # runs the program loop
    while True:
        # easy access to locations of these files
        log_file = os.path.join(this_path, "Logs", time.strftime("%Y-%m-%d %H-%M-%S") + ".txt")
        config_file = os.path.join(this_path, "Config", "config.json")
        control_file = os.path.join(this_path, "Config", "control.json")

        log = _log.Log(log_file) # starts the log

        # tries to read the configuration file
        try:
            config = json.loads(open(config_file, "r").read())
            control = json.loads(open(control_file, "r").read())
        # if the opening of any of these files failed, save the log and stop the execution
        except:
            log.report("[ERROR] could not read config and/or control .json file(s), syntax error of missing file(s)"); log.report("")
            log.open(); log.write(); raise SystemExit

        # validates the config file
        if _validations.validate_config_json(config, log):
            log.report("[ OK  ] config .json load")
        # if the validation failed, save the log and stop the execution
        else:
            log.report("[ERROR] config .json load"); log.report("")
            log.open(); log.write(); raise SystemExit

        # validates the control file
        if _validations.validate_control_json(control, log):
            log.report("[ OK  ] control .json load")
        # if the validation failed, save the log and stop the execution
        else:
            log.report("[ERROR] control .json load"); log.report("")
            log.open(); log.write(); raise SystemExit

        if ast.literal_eval(config["send_email"]):
            # starts the email
            email = _email.Email(
                config["email_sender"],
                config["email_sender_password"],
                _about.EMAIL_SUBJECT,
                "",
                config["email_addressee"])
        else:
            # creates a dummy email where the messages will be written but not sent
            email = _email.Email("", "", "", "", "")

        # registers error occurrence to decide if the log has to be written or the email to be send
        error_flag = False
        # runs the sync defined by every file in the Syncs folder
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(this_path, "Syncs")):
            for file in filenames:
                # maybe stop the program if the last one failed
                # tries to run the sync
                try:
                    # consider only .json files
                    if os.path.splitext(file)[1] == ".json":
                        # if this is the first sync or if the current time exceeds the scheduled time for the sync to occur, then this sync has to run
                        if (os.path.join(dirpath, file) not in control) or (datetime.datetime.now() > datetime.datetime.strptime(control[os.path.join(dirpath, file)], "%Y-%m-%d %H-%M-%S")):
                            # starts the time measurement
                            time_monitor = datetime.datetime.now()

                            log.report("        running: " + os.path.join(dirpath, file))
                            log.report("        loading the .json file...")

                            # tries to load the json file
                            try:
                                sync_properties = json.loads(open(os.path.join(dirpath, file), "r").read())
                                log.report("[ OK  ] sync .json load")
                            # if the load failed, skip this particular sync
                            except:
                                error_flag = True
                                log.report("[ERROR] sync .json load"); log.report("")
                                email.append_message("[ERROR] " + os.path.join(dirpath, file) + ": json load")
                                continue

                            # validates the json file
                            if _validations.validate_sync_json(sync_properties, log):
                                log.report("[ OK  ] .json validation")
                            # if it fails, report the error in the log and the email
                            else:
                                error_flag = True
                                log.report("[ERROR] .json validation"); log.report("")
                                email.append_message("[ERROR] " + os.path.join(dirpath, file) + ": json validation")
                                continue

                            # checks if the sync is enabled
                            if ast.literal_eval(sync_properties["enable"]):
                                log.report("        running the sync job...")
                                # runs the sync
                                if _sync.Sync(sync_properties["source_path"],
                                              sync_properties["source_selection_condition"],
                                              sync_properties["source_maximum_age"],
                                              sync_properties["source_subfolder_search"],
                                              sync_properties["source_filelist_shuffle"],

                                              sync_properties["destination_path"],
                                              sync_properties["destination_selection_condition"],
                                              sync_properties["destination_maximum_age"],
                                              sync_properties["destination_subfolder_search"],
                                              sync_properties["destination_filelist_shuffle"],

                                              sync_properties["hierarchy_maintenance"],
                                              sync_properties["left_files_deletion"],
                                              sync_properties["file_override"],
                                              sync_properties["size_limit"],
                                              log).run():
                                    log.report("[ OK  ] " + os.path.join(dirpath, file))
                                # if the sync returned error, disables the sync to prevent another run until the user takes action
                                else:
                                    error_flag = True

                                    log.report("[ERROR] " + os.path.join(dirpath, file) + ", this sync was disabled"); log.report("")
                                    email.append_message("[ERROR] " + os.path.join(dirpath, file)  + ": sync error. This sync was disabled, please check the logs")
                                    sync_properties["enable"] = "False"

                                    # writes the changes in control json to the file
                                    try:
                                        with open(os.path.join(dirpath, file), "w") as file_to_write:
                                            json.dump(sync_properties, file_to_write, indent=4, ensure_ascii=False)
                                    # if it could not save the json file, stop the execution and send an email alert
                                    except:
                                        log.report("[ERROR] could not write the disable value to the json file"); log.report("")

                                    continue

                                # logs the elapsed time and appends the sync success to the email message
                                log.report("        " + str((datetime.datetime.now() - time_monitor).seconds) + " seconds to sync"); log.report("")
                                email.append_message("[ OK  ] " + os.path.join(dirpath, file))

                                # determines the next datetime to run this sync
                                control[os.path.join(dirpath, file)] = (datetime.datetime.now() + datetime.timedelta(hours=int(sync_properties["sync_cooldown"]))).strftime("%Y-%m-%d %H-%M-%S")
                            # if the sync is disabled
                            else:
                                log.report("        this sync is disabled")
                        # if the sync is still in cooldown time
                        else:
                            log.report("        " + os.path.join(dirpath, file) + " did not run, still in cooldown time")
                # ignores the file if the split was wrong (maybe the file doesnt have an extension)
                except IndexError:
                    continue

        # runs the post sync script if needed
        if "post_sync_script" in config:
            log.report("        running post sync script...")
            post_sync_script_subprocess = subprocess.Popen(config["post_sync_script"], stdout=subprocess.PIPE, shell=True)
            (post_sync_script_output, error_code) = post_sync_script_subprocess.communicate()

            log.report("        the terminal output of the script was as follows:")
            log.report(post_sync_script_output.decode())
        else:
            log.report("        no post sync script specified, skipping...")

        # sends the email if needed
        if ast.literal_eval(config["send_email"]):
            if ast.literal_eval(config["email_only_if_an_error_occur"]):
                if error_flag:
                    log.report("        sending the email...")
                    if email.send():
                        log.report("[ OK  ] email sent")
                    else:
                        log.report("[ERROR] email was not sent")
                else:
                    log.report("        no errors occurred, the email was skipped")
            else:
                log.report("        sending the email...")
                if email.send():
                    log.report("[ OK  ] email sent")
                else:
                    log.report("[ERROR] email was not sent")


        # saves the log if needed
        if ast.literal_eval(config["save_log"]):
            if ast.literal_eval(config["log_only_if_an_error_occur"]):
                if error_flag:
                    try:
                        log.report("        closing the log file.")
                        log.open(); log.write()
                        with open(control_file, "w") as file_to_write:
                            json.dump(control, file_to_write, indent=4, ensure_ascii=False)
                    except:
                        # Maybe send an email here
                        raise SystemExit
            else:
                try:
                    log.report("        closing the log file.")
                    log.open(); log.write()
                    with open(control_file, "w") as file_to_write:
                        json.dump(control, file_to_write, indent=4, ensure_ascii=False)
                except:
                    # Maybe send an email here
                    raise SystemExit


        # deletes file in the Logs folder until the maximum size is satisfied
        if "logs_folder_maximum_size" in config:
            # execute only if the value is greater than zero
            if int(config["logs_folder_maximum_size"]) > 0:

                # maybe this has to be in another place
                def get_folder_size(path):
                    size = 0
                    for (dirpath, dirnames, filenames) in os.walk(path):
                        for f in filenames:
                            size += os.path.getsize(os.path.join(dirpath, f)) / 1024000
                    return size

                # ordenated list of all files in Logs
                path = os.path.join(this_path, "Logs")
                # sorts the files by modified date
                files = sorted(os.listdir(path), key=lambda x: os.stat(os.path.join(path, x)).st_mtime)
                # for every file in the Logs folder
                for f in files:
                    # if the total size is greater than the maximum allowed
                    if get_folder_size(path) > int(config["logs_folder_maximum_size"]):
                        # removes the current file and tests again
                        if os.path.isfile(os.path.join(path, f)): os.remove(os.path.join(path, f))


        # resets the flag
        error_flag = False

        # sleeps until the next check time, given by check_cooldown
        time.sleep(int(config["check_cooldown"]) * 60 * 60)