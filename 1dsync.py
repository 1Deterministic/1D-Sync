import _log
import _sync
import _validations
import _email
import _about

import os
import json
import time
import datetime
import logging
import random


if __name__ == "__main__":
    # hides eyed3 logs on terminal
    logging.getLogger("eyed3").setLevel(logging.CRITICAL)

    # stores the path of the current directory
    #this_path = os.path.dirname(__file__)
    this_path = os.getcwd()

    # repeats forever
    while True:
        # easy access to locations of these files
        log_file = os.path.join(this_path, "Logs", time.strftime("%Y-%m-%d %H-%M-%S") + ".txt")
        config_file = os.path.join(this_path, "Config", "config.json")
        control_file = os.path.join(this_path, "Config", "control.json")

        # starts the log
        log = _log.Log(log_file)

        # reads the configuration file
        try:
            config = json.loads(open(config_file, "r").read())
            control = json.loads(open(control_file, "r").read())

            # checks if config.json did not pass the validation
            if not _validations.validate_config_json(config):
                log.report("[ERROR] config .json load"); log.report("")
                log.open()
                log.write()
                raise SystemExit
            else:
                log.report("[ OK  ] config .json load")

            # checks if control.json did not pass the validation
            if not _validations.validate_control_json(control):
                log.report("[ERROR] control .json load"); log.report("")
                log.open()
                log.write()
                raise SystemExit
            else:
                log.report("[ OK  ] control .json load")

        # if some other error occurred
        except:
            log.report("[ERROR] config/control .json load"); log.report("")
            log.open()
            log.write()
            raise SystemExit

        # starts the email
        email = _email.Email(config["email_sender"], config["email_sender_password"], _about.EMAIL_SUBJECT, "", config["email_addressee"])

        # walks the Syncs folder
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(this_path, "Syncs")):
            # for every file inside the Syncs folder
            for file in filenames:
                try:
                    # consider only .json files
                    if os.path.splitext(file)[1] == ".json":
                        # if this is the first sync or if the current time exceeds the scheduled time for the sync to occur
                        if (os.path.join(dirpath, file) not in control) or (datetime.datetime.now() > datetime.datetime.strptime(control[os.path.join(dirpath, file)], "%Y-%m-%d %H-%M-%S")):
                            # this sync has to run

                            # starts the time measure
                            time_monitor = datetime.datetime.now()

                            log.report("        running: " + os.path.join(dirpath, file))

                            log.report("        loading the .json file...")
                            try:
                                # loads its .json
                                sync_properties = json.loads(open(os.path.join(dirpath, file), "r").read())
                                log.report("[ OK  ] sync .json load")
                            except:
                                log.report("[ERROR] sync .json load"); log.report("")
                                email.append_message("[ERROR] " + os.path.join(dirpath, file) + ": json load")
                                continue

                            # tests the json read
                            if _validations.validate_sync_json(sync_properties):
                                log.report("[ OK  ] .json validation")
                            else:
                                log.report("[ERROR] .json validation"); log.report("")
                                email.append_message("[ERROR] " + os.path.join(dirpath, file) + ": json validation")
                                continue

                            # if the sync is enabled
                            if sync_properties["enable"] == "True":
                                log.report("        running the sync job...")
                                # runs the sync
                                if _sync.Sync(sync_properties["source_path"],
                                              sync_properties["source_selection_condition"],
                                              sync_properties["source_subfolder_search"],
                                              sync_properties["source_filelist_shuffle"],
                                              sync_properties["destination_path"],
                                              sync_properties["destination_selection_condition"],
                                              sync_properties["destination_subfolder_search"],
                                              sync_properties["destination_filelist_shuffle"],
                                              sync_properties["hierarchy_maintenance"],
                                              sync_properties["left_files_deletion"],
                                              sync_properties["file_override"],
                                              sync_properties["size_limit"],
                                              log).run():
                                    log.report("[ OK  ] " + os.path.join(dirpath, file))
                                else:
                                    log.report("[ERROR] " + os.path.join(dirpath, file)); log.report("")
                                    email.append_message("[ERROR] " + os.path.join(dirpath, file)  + ": sync error. This sync was disabled, please check the logs")
                                    sync_properties["enable"] = "False"
                                    try:
                                        # writes the changes in control json to the file
                                        with open(os.path.join(dirpath, file), "w") as file_to_write:
                                            json.dump(sync_properties, file_to_write, indent=4, ensure_ascii=False)

                                    except:
                                        email.append_message("Unespected close, please check the logs")
                                        email.send()
                                        raise SystemExit

                                    continue

                                log.report("        " + str((datetime.datetime.now() - time_monitor).seconds) + " seconds to sync"); log.report("")
                                email.append_message("[ OK  ] " + os.path.join(dirpath, file))

                                # determines the next datetime to run this sync
                                sync_cooldown_range = sync_properties["sync_cooldown"].split("-")
                                cooldown = random.randint(int(sync_cooldown_range[0]), int(sync_cooldown_range[1]))

                                # updates the next run datetime
                                control[os.path.join(dirpath, file)] = (datetime.datetime.now() + datetime.timedelta(hours=cooldown)).strftime("%Y-%m-%d %H-%M-%S")

                            # if the sync is disabled
                            else:
                                log.report("        this sync is disabled")

                        # if the sync is still in cooldown time
                        else:
                            log.report("        " + os.path.join(dirpath, file) + " did not run, still in cooldown time")

                # ignores the file if the split was wrong (maybe the file doesnt have an extension)
                except IndexError:
                    pass

        try:
            # commits the log file if needed
            log.open()
            log.write()

            # sends the email if needed
            if not email.is_empty():
                email.send()

            # writes the changes in control json to the file
            with open(control_file, "w") as file_to_write:
                json.dump(control, file_to_write, indent=4, ensure_ascii=False)

        except:
            # if the log was not saved, try to send an email
            email.append_message("Unespected close, please check the logs")
            email.send()
            raise SystemExit

        # sleeps until the next check time, given by check_cooldown
        time.sleep(int(config["check_cooldown"]) * 60 * 60)