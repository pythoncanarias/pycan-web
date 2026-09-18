#!/usr/bin/env python3

"""

# Source - https://stackoverflow.com/a/52105406
# Posted by Joao Coelho
# Retrieved 2026-09-17, License - CC BY-SA 4.0
"""

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import boto3

def create_multipart_message(
        sender: str,
        recipients: list,
        title: str,
        text: str=None,
        html: str=None,
        attachments: list=None) -> MIMEMultipart:
    """
    Creates a MIME multipart message object.
    Uses only the Python `email` standard library.
    Emails, both sender and recipients, can be just the email
    string or have the format 'The Name <the_email@host.com>'.

    :param sender: The sender.

    :param recipients: List of recipients. Needs to be a list, even if only one recipient.

    :param title: The title of the email.

    :param text: The text version of the email body (optional).

    :param html: The html version of the email body (optional).

    :param attachments: List of files to attach in the email.

    :return: A `MIMEMultipart` to be used to send the email.
    """
    multipart_content_subtype = 'alternative' if text and html else 'mixed'
    msg = MIMEMultipart(multipart_content_subtype)
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    # Record the MIME types of both parts - text/plain and text/html.
    # According to RFC 2046, the last part of a multipart message, in
    # this case the HTML message, is best and preferred.
    if text:
        part = MIMEText(text, 'plain')
        msg.attach(part)
    if html:
        part = MIMEText(html, 'html')
        msg.attach(part)
    for attachment in attachments or []:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(attachment),
                )
            msg.attach(part)
    return msg


def send_mail(
        sender: str,
        recipients: list,
        title: str,
        text: str=None,
        html: str=None,
        attachments: list=None) -> dict:
    """
    Send email to recipients. Sends one mail to all recipients.
    The sender needs to be a verified email in SES.
    """
    msg = create_multipart_message(sender, recipients, title, text, html, attachments)
    ses_client = boto3.client('ses')  # Use your settings here
    for email in recipients:
        ses_client.verify_email_identity(EmailAddress=email)
    return ses_client.send_raw_email(
        Source=sender,
        Destinations=recipients,
        RawMessage={'Data': msg.as_string()}
        )


if __name__ == '__main__':
    sender_ = 'Python Canarias <info@pythoncanarias.es>'
    recipients = [
        'Juan I. <euribates@email.com>',
        'jrodleo@gobiernodecanarias.org',
        ]

    title_ = 'Prueba desde Amazon SES'
    text_ = 'The text version\nwith multiple lines.'
    body_ = """<html><head></head><body><h1>A header 1</h1><br>Some text."""
    response = send_mail(sender_, recipients, title_, text_, body_)
    print(response)

