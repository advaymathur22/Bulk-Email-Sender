import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL, PASSWORD, SMTP_SERVER, SMTP_PORT


class EmailSender:
    def __init__(self):
        self.email = EMAIL
        self.password = PASSWORD
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT

    def send_bulk_emails(self, recipients_file, subject_template, body_template):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)

            with open(recipients_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row.get('name', '').strip()
                    club_name = row.get('club_name', '').strip()
                    email_addr = row.get('email', '').strip()
                    if not email_addr:
                        continue

                    subject = (subject_template
                               .replace('[NAME]', name)
                               .replace('[CLUB_NAME]', club_name)
                               .replace('[EMAIL]', email_addr))

                    body = (body_template
                            .replace('[NAME]', name)
                            .replace('[CLUB_NAME]', club_name)
                            .replace('[EMAIL]', email_addr))

                    msg = MIMEMultipart()
                    msg['From'] = self.email
                    msg['To'] = email_addr
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))

                    try:
                        server.send_message(msg)
                        print(f"Sent to {email_addr}")
                    except Exception as e:
                        print(f"Failed to send to {email_addr}: {e}")

                    time.sleep(1)


if __name__ == "__main__":
    sender = EmailSender()

    subject = "Youth Sports Operations With Waresport"
    body = """Hello [NAME],

I hope you're doing well! I'm reaching out to introduce our youth sports operations platform — 
built specifically for organizations like yours that manage teams, schedules, registrations, and communication all in one place.
We're already helping clubs across the region streamline their operations and make them more scalable. 
We'd love to explore how we can support [CLUB_NAME] as well. 
Would you be open to a quick call or demo? 
I'd be happy to walk you through how it works and how it can support your goals.

Best regards, 

"""
    sender.send_bulk_emails("recipients.csv", subject, body)


