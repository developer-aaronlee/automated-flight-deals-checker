from twilio.rest import Client
import smtplib

account_sid = "AC5fa6c5a6eb0469ffa205f93d360898f4"
auth_token = "533ee0c3d029a4b23806b2991338307f"

my_email = "pythonautomationapp@gmail.com"
password = "dxabiogqxlleamrw"


class NotificationManager:

    def __init__(self):
        self.client = Client(account_sid, auth_token)
        self.connection = None

    def send_message(self, alert):
        message = self.client.messages.create(
            body=alert,
            from_="+14422410317",
            to="+16078787777"
        )
        print(message.body)
        print(message.status)

    def send_email(self, recipients, alert, booking_link):
        with smtplib.SMTP("smtp.gmail.com", port=587) as self.connection:
            self.connection.starttls()
            self.connection.login(user=my_email, password=password)
            for x in recipients:
                self.connection.sendmail(from_addr=my_email, to_addrs=x,
                                         msg=f"Subject: New Low Price Flight!\n\n{alert}\n{booking_link}".encode("utf-8"))

