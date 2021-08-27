import os
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

from config import email as config


class SendEmail:
    def __init__(self):
        self.TEMPLATE_DIR = os.path.abspath(os.path.dirname(__file__))
        self.msg = EmailMessage()
        self.msg['From'] = Address(
            config.EMAIL_USER_NAME, config.EMAIL_USER_NAME, config.EMAIL_USER)

    def send_custom_email(self, msg, to_email):
        # creates SMTP session
        s = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        # sending the mail
        s.send_message(msg, config.EMAIL_USER, to_email)
        # terminating the session
        s.quit()

    def activate_account_email(self, to_email, name, activation_link):
        self.msg['Subject'] = "Welcome to SweetVendors"
        self.msg['To'] = (
            Address(name, name, to_email),
        )

        template_name = os.path.join(
            self.TEMPLATE_DIR, "templates", "activateaccount.html")
        with open(template_name) as file:
            html = file.read()

        html = html.replace("##USERNAME##", name).replace(
            "##ACTIVATION_LINK##", activation_link)

        self.msg.add_alternative(html, subtype='html')
        self.send_custom_email(self.msg, to_email)

    def pwd_reset_email(self, to_email, name, reset_link):
        self.msg['Subject'] = "SweetVendors: Password Reset"
        self.msg['To'] = (
            Address(name, name, to_email),
        )

        template_name = os.path.join(
            self.TEMPLATE_DIR, "templates", "resetpassword.html")
        with open(template_name) as file:
            html = file.read()

        html = html.replace("##USERNAME##", name).replace(
            "##PASSWORD_RESET_LINK##", reset_link)

        self.msg.add_alternative(html, subtype='html')
        self.send_custom_email(self.msg, to_email)
