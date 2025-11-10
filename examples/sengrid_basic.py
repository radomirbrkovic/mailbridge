"""
SendGrid Provider - Basic Email Example

This example shows how to send basic emails using SendGrid.
"""

from mailbridge import MailBridge

# Initialize SendGrid provider
mailer = MailBridge(
    provider='sendgrid',
    api_key='your-sendgrid-api-key',
    from_email='noreply@yourcompany.com'  # Optional default sender
)

# Example 1: Simple HTML email
print("Example 1: Simple HTML email")
response = mailer.send(
    to='recipient@example.com',
    subject='Welcome to Our Service',
    body='<h1>Hello!</h1><p>Thanks for signing up.</p>',
    html=True
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 2: Plain text email
print("Example 2: Plain text email")
response = mailer.send(
    to='recipient@example.com',
    subject='Plain Text Message',
    body='This is a plain text email without HTML formatting.',
    html=False
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 3: Email with CC and BCC
print("Example 3: Email with CC and BCC")
response = mailer.send(
    to='recipient@example.com',
    subject='Team Update',
    body='<p>Here is the latest team update...</p>',
    cc=['manager@example.com', 'team-lead@example.com'],
    bcc=['admin@example.com']
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 4: Email with custom headers
print("Example 4: Email with custom headers")
response = mailer.send(
    to='recipient@example.com',
    subject='Marketing Campaign',
    body='<p>Special offer just for you!</p>',
    headers={
        'X-Campaign-ID': 'summer-2024',
        'X-Priority': '1'
    },
    tags=['marketing', 'summer-campaign']  # For tracking
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 5: Email with attachments
print("Example 5: Email with attachments")
from pathlib import Path

# Assuming you have a file
attachment_path = Path('invoice.pdf')
if attachment_path.exists():
    response = mailer.send(
        to='recipient@example.com',
        subject='Your Invoice',
        body='<p>Please find your invoice attached.</p>',
        attachments=[attachment_path]
    )
    print(f"✓ Sent with attachment! Message ID: {response.message_id}")
else:
    print("⚠ Skipping attachment example (file not found)")
print()


# Example 6: Multiple recipients
print("Example 6: Multiple recipients")
response = mailer.send(
    to=[
        'user1@example.com',
        'user2@example.com',
        'user3@example.com'
    ],
    subject='Team Announcement',
    body='<h2>Important Update</h2><p>Please review the attached documents.</p>'
)
print(f"✓ Sent to multiple recipients! Message ID: {response.message_id}")
print()


# Example 7: Using context manager (auto-close)
print("Example 7: Using context manager")
with MailBridge(provider='sendgrid', api_key='your-api-key') as mailer:
    response = mailer.send(
        to='recipient@example.com',
        subject='Auto-closed Connection',
        body='<p>Connection will be closed automatically.</p>'
    )
    print(f"✓ Sent! Message ID: {response.message_id}")
# Connection automatically closed here
print()


print("=" * 60)
print("All SendGrid basic examples completed!")
print("=" * 60)