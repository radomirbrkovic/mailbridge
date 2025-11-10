"""
SMTP Provider - Basic Email Example

This example shows how to send emails using any SMTP server.
Works with Gmail, Outlook, custom servers, etc.
"""

from mailbridge import MailBridge

# Example 1: Gmail SMTP
print("Example 1: Gmail SMTP")
gmail_mailer = MailBridge(
    provider='smtp',
    host='smtp.gmail.com',
    port=587,
    username='your-email@gmail.com',
    password='your-app-password',  # Use App Password, not regular password
    from_email='your-email@gmail.com',
    use_tls=True
)

response = gmail_mailer.send(
    to='recipient@example.com',
    subject='Test from Gmail',
    body='<p>This email was sent via Gmail SMTP.</p>'
)
print(f"✓ Sent via Gmail! Message ID: {response.message_id}")
print()


# Example 2: Outlook/Office365 SMTP
print("Example 2: Outlook SMTP")
outlook_mailer = MailBridge(
    provider='smtp',
    host='smtp.office365.com',
    port=587,
    username='your-email@outlook.com',
    password='your-password',
    from_email='your-email@outlook.com',
    use_tls=True
)

response = outlook_mailer.send(
    to='recipient@example.com',
    subject='Test from Outlook',
    body='<p>This email was sent via Outlook SMTP.</p>'
)
print(f"✓ Sent via Outlook! Message ID: {response.message_id}")
print()


# Example 3: Custom SMTP server
print("Example 3: Custom SMTP server")
custom_mailer = MailBridge(
    provider='smtp',
    host='mail.yourdomain.com',
    port=587,
    username='your-username',
    password='your-password',
    from_email='noreply@yourdomain.com',
    use_tls=True
)

response = custom_mailer.send(
    to='recipient@example.com',
    subject='Test from Custom Server',
    body='<p>This email was sent via custom SMTP server.</p>'
)
print(f"✓ Sent via custom server! Message ID: {response.message_id}")
print()


# Example 4: SMTP with SSL (port 465)
print("Example 4: SMTP with SSL")
ssl_mailer = MailBridge(
    provider='smtp',
    host='smtp.example.com',
    port=465,
    username='your-username',
    password='your-password',
    from_email='noreply@example.com',
    use_ssl=True  # Use SSL instead of TLS
)

response = ssl_mailer.send(
    to='recipient@example.com',
    subject='Test with SSL',
    body='<p>This email uses SSL encryption.</p>'
)
print(f"✓ Sent via SSL! Message ID: {response.message_id}")
print()


# Example 5: Plain text email
print("Example 5: Plain text email")
response = gmail_mailer.send(
    to='recipient@example.com',
    subject='Plain Text',
    body='This is a plain text email.',
    html=False
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 6: Email with CC and BCC
print("Example 6: Email with CC and BCC")
response = gmail_mailer.send(
    to='recipient@example.com',
    subject='Team Update',
    body='<p>Update for the team...</p>',
    cc=['teammate@example.com'],
    bcc=['manager@example.com']
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 7: Email with attachments
print("Example 7: Email with attachments")
from pathlib import Path

attachment_path = Path('report.pdf')
if attachment_path.exists():
    response = gmail_mailer.send(
        to='recipient@example.com',
        subject='Report Attached',
        body='<p>Please find the report attached.</p>',
        attachments=[attachment_path]
    )
    print(f"✓ Sent with attachment! Message ID: {response.message_id}")
else:
    print("⚠ Skipping attachment example (file not found)")
print()


# Example 8: Email with Reply-To
print("Example 8: Email with Reply-To")
response = gmail_mailer.send(
    to='recipient@example.com',
    subject='Customer Support',
    body='<p>Reply to this email for support.</p>',
    reply_to='support@example.com'
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 9: Email with custom headers
print("Example 9: Email with custom headers")
response = gmail_mailer.send(
    to='recipient@example.com',
    subject='Newsletter',
    body='<p>Monthly newsletter...</p>',
    headers={
        'X-Campaign-ID': 'newsletter-2024',
        'X-Mailer': 'MailBridge'
    }
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 10: No authentication (local server)
print("Example 10: Local SMTP without authentication")
local_mailer = MailBridge(
    provider='smtp',
    host='localhost',
    port=25,
    from_email='test@localhost'
    # No username/password needed for local server
)

try:
    response = local_mailer.send(
        to='recipient@example.com',
        subject='Test from Local',
        body='<p>Sent from local SMTP server.</p>'
    )
    print(f"✓ Sent via local server! Message ID: {response.message_id}")
except Exception as e:
    print(f"⚠ Local server not available: {e}")
print()


print("=" * 60)
print("All SMTP examples completed!")
print()
print("📝 SMTP Configuration Tips:")
print()
print("Gmail:")
print("  • Use App Password (not regular password)")
print("  • Enable 2FA and generate App Password")
print("  • Host: smtp.gmail.com, Port: 587, TLS: True")
print()
print("Outlook/Office365:")
print("  • Host: smtp.office365.com, Port: 587, TLS: True")
print()
print("Yahoo:")
print("  • Host: smtp.mail.yahoo.com, Port: 587, TLS: True")
print()
print("Port Guide:")
print("  • 25: Standard (often blocked)")
print("  • 587: TLS (recommended)")
print("  • 465: SSL")
print("  • 2525: Alternative to 587")
print("=" * 60)