import imaplib
import email
import os
import json
import magic  # Make sure to install this library using: pip install python-magic

# Load environment variables
keys = json.load(open('info.json'))
IMAP_SSL_HOST = keys["host"]
IMAP_SSL_PORT = keys["port"]
EMAIL = keys["email"]
PASSWORD = keys["password"]

def download_attachments(msg, output_folder="."):
    for part in msg.walk():
        #print(part)
        filename = part.get_filename()
        print("FILENAME",filename)
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        
        if filename:
            file_content = part.get_payload(decode=True)
            file_type = magic.Magic()
            mime_type = file_type.from_buffer(file_content)

            # Create a subfolder based on MIME type
            mime_type_folder = os.path.join(output_folder, mime_type.replace("/", "_"))
            os.makedirs(mime_type_folder, exist_ok=True)

            filepath = os.path.join(mime_type_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(file_content)
            print(f"Attachment '{filename}' of type '{mime_type}' downloaded to '{mime_type_folder}'")

def read_email_and_download_attachments():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SSL_HOST, IMAP_SSL_PORT)

    # Login to the email account
    mail.login(EMAIL, PASSWORD)

    # Select the mailbox you want to read emails from
    mail.select("inbox")

    # Search for all emails in the mailbox
    result, data = mail.search(None, "ALL")

    # Get the latest email ID
    latest_email_id = data[0].split()[-1]

    # Fetch the email by ID
    result, message_data = mail.fetch(latest_email_id, "(RFC822)")

    # Get the email content
    raw_email = message_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Download attachments
    download_attachments(msg)

    # Logout from the email account
    mail.logout()


read_email_and_download_attachments()
