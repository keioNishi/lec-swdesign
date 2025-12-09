# -*- coding: utf-8 -*-
"""
Email Client Demo - Fixed Version
電子メール（Email）プロトコルの基礎とクライアント実装（修正版）
"""

import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import os
import time


class EmailClientDemo:
    """Simple email client demonstration (fixed version)"""

    def __init__(self):
        # Demo settings (change for actual use)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def create_simple_email(self, sender, recipient, subject, body):
        """Create simple text email"""
        print("=== Simple Email Creation ===")

        # Create MIMEText object (text email)
        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        print(f"Sender: {sender}")
        print(f"Recipient: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:50]}...")

        # Get email content as string
        email_content = message.as_string()
        print(f"\nEmail size: {len(email_content)} bytes")

        return message

    def create_html_email(self, sender, recipient, subject, html_body):
        """Create HTML email"""
        print("\n=== HTML Email Creation ===")

        # Create multipart message
        message = MIMEMultipart('alternative')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        # Add HTML content
        html_part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(html_part)

        print(f"HTML email created")
        print(f"Subject: {subject}")

        return message

    def create_multipart_email(self, sender, recipient, subject, text_body, html_body):
        """Create multipart email with both text and HTML"""
        print("\n=== Multipart Email Creation ===")

        # Create multipart message
        message = MIMEMultipart('alternative')
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        # Add text version
        text_part = MIMEText(text_body, 'plain', 'utf-8')
        message.attach(text_part)

        # Add HTML version
        html_part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(html_part)

        print(f"Multipart email created")
        print(f"Text part: {len(text_body)} characters")
        print(f"HTML part: {len(html_body)} characters")

        return message

    def add_attachment_to_email(self, sender, recipient, subject, body, attachment_name="dummy_file.txt"):
        """Create email with attachment (fixed implementation)"""
        print(f"\n=== Email with Attachment Creation ===")

        # Create multipart message for attachments
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject

        # Add main body
        body_part = MIMEText(body, 'plain', 'utf-8')
        message.attach(body_part)

        # Create dummy file content if file doesn't exist
        if not os.path.exists(attachment_name):
            dummy_content = f"This is dummy attachment data for {attachment_name}.\nCreated for demo purposes.\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            file_data = dummy_content.encode('utf-8')
        else:
            with open(attachment_name, 'rb') as f:
                file_data = f.read()

        # Create attachment part
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)

        # Add header for attachment
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_name}'
        )

        # Attach to message
        message.attach(attachment)

        print(f"Attachment '{attachment_name}' added")
        print(f"File size: {len(file_data)} bytes")

        return message

    def simulate_smtp_send(self, message):
        """Simulate SMTP sending (without actually sending)"""
        print("\n=== SMTP Send Simulation ===")

        try:
            # Display email content
            email_content = message.as_string()

            print("--- Email Headers ---")
            print(f"From: {message['From']}")
            print(f"To: {message['To']}")
            print(f"Subject: {message['Subject']}")
            print(f"Date: {message.get('Date', 'Not set')}")

            print("\n--- Email Body (first 200 characters) ---")
            # Find body start
            body_start = email_content.find('\r\n\r\n')
            if body_start == -1:
                body_start = email_content.find('\n\n')

            if body_start != -1:
                body = email_content[body_start + 4:body_start + 204]
                print(body + "..." if len(body) == 200 else body)

            print(f"\nTotal email size: {len(email_content)} bytes")
            print("[OK] Email send simulation completed")

            return True

        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            return False

    def simulate_pop3_receive(self):
        """Simulate POP3 receiving"""
        print("\n=== POP3 Receive Simulation ===")

        # Create dummy email data
        dummy_emails = [
            {
                'from': 'sender1@example.com',
                'subject': 'Test Email 1',
                'body': 'This is the first test email.',
                'date': '2024-03-15 10:00:00'
            },
            {
                'from': 'sender2@example.com',
                'subject': 'Important Notice',
                'body': 'This is an important notice. Please review.',
                'date': '2024-03-15 11:30:00'
            },
            {
                'from': 'newsletter@example.com',
                'subject': 'Monthly Newsletter',
                'body': 'Here is this month\'s newsletter.',
                'date': '2024-03-15 09:15:00'
            }
        ]

        print(f"Received emails: {len(dummy_emails)}")
        print("\n--- Received Email List ---")

        for i, mail in enumerate(dummy_emails, 1):
            print(f"\nEmail {i}:")
            print(f"  From: {mail['from']}")
            print(f"  Subject: {mail['subject']}")
            print(f"  Date: {mail['date']}")
            print(f"  Body: {mail['body'][:30]}...")

        return dummy_emails

    def parse_email_headers(self):
        """Email header parsing demo"""
        print("\n=== Email Header Parsing ===")

        # Create sample email
        sample_email = """From: sender@example.com
To: recipient@example.com
Subject: Test Email Message
Date: Fri, 15 Mar 2024 10:00:00 +0900
Message-ID: <12345@example.com>
Content-Type: text/plain; charset=utf-8

This is a sample email body.
It contains multiple lines of text.
"""

        # Create email object
        msg = email.message_from_string(sample_email)

        print("--- Parsing Results ---")
        print(f"From: {msg['From']}")
        print(f"To: {msg['To']}")
        print(f"Subject: {msg['Subject']}")
        print(f"Date: {msg['Date']}")
        print(f"Message-ID: {msg['Message-ID']}")
        print(f"Content-Type: {msg['Content-Type']}")

        # Get email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8')
                    print(f"\nBody:\n{body}")
                    break
        else:
            body = msg.get_payload()
            print(f"\nBody:\n{body}")

    def create_test_attachment_file(self, filename="25_test_attachment.txt"):
        """Create a test attachment file"""
        print(f"\n=== Creating Test Attachment File: {filename} ===")

        content = f"""Test Attachment File
Created for Email Demo
=====================

This is a test attachment file created for demonstrating email attachments.

Filename: {filename}
Created: {time.strftime('%Y-%m-%d %H:%M:%S')}
Purpose: Educational demonstration

Content includes:
- Text data
- Timestamp information
- File metadata

This file can be safely deleted after the demo.
"""

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Test file '{filename}' created successfully")
            print(f"File size: {len(content)} characters")
            return filename
        except Exception as e:
            print(f"[ERROR] Failed to create test file: {e}")
            return None


def main():
    """Main demo function"""
    print("Email Protocol Basic Demo (Fixed Version)")
    print("=" * 50)

    client = EmailClientDemo()

    # 1. Create simple text email
    simple_mail = client.create_simple_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="Test Email",
        body="This is a test email body.\nIt includes line breaks."
    )

    # 2. Create HTML email
    html_body = """
    <html>
    <body>
        <h1>HTML Email Test</h1>
        <p>This is an <strong>HTML format</strong> email.</p>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
    </body>
    </html>
    """

    html_mail = client.create_html_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="HTML Test Email",
        html_body=html_body
    )

    # 3. Create multipart email
    text_body = "This is the text version of the email."
    multipart_mail = client.create_multipart_email(
        sender="test@example.com",
        recipient="recipient@example.com",
        subject="Multipart Test",
        text_body=text_body,
        html_body=html_body
    )

    # 4. Create test attachment file
    test_file = client.create_test_attachment_file()

    # 5. Create email with attachment (fixed implementation)
    if test_file:
        attachment_mail = client.add_attachment_to_email(
            sender="test@example.com",
            recipient="recipient@example.com",
            subject="Email with Attachment",
            body="This email contains an attachment.",
            attachment_name=test_file
        )
    else:
        attachment_mail = client.add_attachment_to_email(
            sender="test@example.com",
            recipient="recipient@example.com",
            subject="Email with Dummy Attachment",
            body="This email contains a dummy attachment."
        )

    # 6. SMTP send simulation
    client.simulate_smtp_send(multipart_mail)

    # 7. POP3 receive simulation
    received_emails = client.simulate_pop3_receive()

    # 8. Email header parsing
    client.parse_email_headers()

    print("\n" + "=" * 50)
    print("Email demo completed")
    print("\nNote: This demo is for educational purposes.")
    print("Actual email sending requires proper authentication and security settings.")

    # Clean up test file
    if test_file and os.path.exists(test_file):
        try:
            os.remove(test_file)
            print(f"\nTest file '{test_file}' cleaned up.")
        except:
            print(f"\nNote: You may manually delete '{test_file}' if needed.")


if __name__ == "__main__":
    main()