import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(recipient_email, subject, body):
    """
    Sends an email using the specified SMTP server.

    Parameters:
    recipient_email (str): The email address of the recipient.
    subject (str): The subject of the email.
    body (str): The body of the email, in HTML format.

    Returns:
    None
    """
    # Parameters
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PWD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body, subtype='html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Identify ourselves to the SMTP server
            server.starttls()  # Secure the connection
            server.ehlo()
            # Log in to your email account
            server.login(sender_email, sender_password)
            # Send the email
            server.send_message(msg)
            print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred: {e}')
