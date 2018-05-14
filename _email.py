import _about

import smtplib
from email.message import EmailMessage

class Email:
    # creates an email object
    def __init__(self, sender, password, subject, message, addressee):
        # stores the server address
        self.server_address = "smtp.gmail.com: 587"
        # stores the sender
        self.sender = sender
        # stores the password of the sender
        self.password = password
        # stores the subject of the message
        self.subject = subject
        # stores the message
        self.message = message
        # stores the addressee
        self.addressee = addressee

    # sends this email
    def send(self):
        # tries to send the email
        try:
            email_msg = EmailMessage()
            email_msg.set_content(_about.EMAIL_HEADER + self.message)

            email_msg['Subject'] = self.subject
            email_msg['From'] = self.sender
            email_msg['To'] = self.addressee

            server = smtplib.SMTP(self.server_address)
            server.connect(self.server_address)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender, self.password)
            server.send_message(email_msg)

            server.quit()

            # if the email was send, return success
            return True

        # if something went wrong
        except:
            # returns error
            return False


    def append_message(self, text):
        self.message += text + "\n"

    def is_empty(self):
        return self.message == ""
