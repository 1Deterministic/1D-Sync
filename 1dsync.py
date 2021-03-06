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
        log = _log.Log(root) # logs all program operations
        config = _config.Config(root) # main configuration file
        control = _control.Control(root) # controls the sync schedule
        email = _email.Email()  # email sent to the user, if asked

        if not config.load(log): # loads the main config file
            raise SystemExit # force close if an error occurred

        if not control.load(log): # loads the schedule file
            raise SystemExit # force close if an error occurred

        if first_run: # will sleep the startup delay if this is the first program loop
            first_run = False
            config.run_startup_delay(log)

        log.report("") # indentation of the log file
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(root, _paths.syncs_folder)): # runs every sync found
            for file in filenames:
                if os.path.splitext(file)[1] == ".json":
                    sync = _sync.Sync(os.path.join(dirpath, file))  # initializes the sync

                    if (not sync.load(log)) or (not sync.run(control, log)): # loads and runs the sync
                        if not sync.disable(log): # an error in trying to disable the sync will force close the program
                            raise SystemExit

                log.report("")  # indentation of the log file

        config.run_post_sync_script(log) # runs the post sync script

        email.append_message(log.get_content())
        config.send_email(email, log) # sends the email, if necessary

        if not control.write(log): # writes the schedule file
            raise SystemExit  # force close if an error occurred

        if not config.save_log(log): # saves the log
            raise SystemExit # force close if an error occurred

        if not config.run_check_cooldown(): # sleeps the program the specified amount of time
            raise SystemExit