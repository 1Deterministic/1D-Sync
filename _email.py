'''

This builds an email message and send it

'''

import _strings

import smtplib
from email.message import EmailMessage

class Email:
    def __init__(self): # test in Tests/Unit/test_email.test_init
        self.message = "" # initializes the email with an empty message

    # sends the email
    def send(self, sender, password, addressee, log): # test in Tests/Unit/test_email.test_send
        server_address = "smtp.gmail.com: 587"

        try:
            email_msg = EmailMessage()
            email_msg.set_content(self.message)

            email_msg['Subject'] = _strings.strings["email_subject"]
            email_msg['From'] = sender
            email_msg['To'] = addressee

            server = smtplib.SMTP(server_address)
            server.connect(server_address)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.send_message(email_msg)
            server.quit()

            log.report("ok_email_send", detail=addressee)
            return True

        except:
            log.report("error_email_send", detail=addressee)
            return False

    def append_message(self, text): # test in Tests/Unit/test_email.test_append_message
        self.message += text
