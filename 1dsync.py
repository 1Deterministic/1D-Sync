'''

Main program file

'''

import _log
import _sync
import _email
import _config
import _control
import _paths

import os
import logging


if __name__ == "__main__":
    logging.getLogger("eyed3").setLevel(logging.CRITICAL) # hides the eyed3 console output

    root = os.path.dirname(os.path.realpath(__file__)) # filesystem path to this python file

    first_run = True # helps with the startup delay

    while True:
        error_flag = False

        log = _log.Log(root) # logs all program operations
        email = _email.Email() # email sent to the user, if asked
        config = _config.Config(root) # main configuration file
        control = _control.Control(root) # controls the sync schedule

        if not config.load(log): # loads the main config file
            raise SystemExit # force close if an error occurred

        if not control.load(log): # loads the schedule file
            raise SystemExit # force close if an error occurred

        if first_run: # will sleep the startup delay if this is the first program loop
            first_run = False
            config.run_startup_delay(log)

        for (dirpath, dirnames, filenames) in os.walk(os.path.join(root, _paths.syncs_folder)): # runs every sync found
            for file in filenames:
                if os.path.splitext(file)[1] == ".json":
                    sync = _sync.Sync(os.path.join(dirpath, file))  # initializes the sync

                    if (not sync.load(log)) or (not sync.run(control, log)): # loads and runs the sync
                        # will enter here if any of the above operations returns an error
                        error_flag = True

                        if not sync.disable(log): # an error in trying to disable the sync will force close the program
                            raise SystemExit

                        email.append_message("[ERROR] " + os.path.join(dirpath, file)) # reports the error in the email
                        continue # once this problematic sync is successfully disabled, moves to the next one

                    email.append_message("[ OK  ] " + os.path.join(dirpath, file)) # reports the sync success in the email

        config.run_post_sync_script(log) # runs the post sync script
        
        config.send_email(email, error_flag, log) # sends the email, if necessary

        if not control.write(log): # writes the schedule file
            raise SystemExit  # force close if an error occurred

        if not config.save_log(error_flag, log): # saves the log
            raise SystemExit # force close if an error occurred

        if not config.run_logs_folder_maximum_size(root): # deletes old log files to meet the specified maximum folder size
            raise SystemError # force close if an error occurred

        config.run_check_cooldown() # sleeps the program the specified amount of time