"""
Postmark Provider - Basic Email Example

This example shows how to send basic emails using Postmark.
"""

from mailbridge import MailBridge

# Initialize Postmark provider
mailer = MailBridge(
    provider='postmark',
    server_token='your-postmark-server-token',
    from_email='verified@yourdomain.com'  # Must be verified in Postmark
)

# Example 1: Simple email
print("Example 1: Simple HTML email")
response = mailer.send(
    to='recipient@example.com',
    subject='Welcome to Our Service',
    body='<h1>Hello from Postmark!</h1><p>Great deliverability.</p>',
    html=True
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 2: Plain text email
print("Example 2: Plain text email")
response = mailer.send(
    to='recipient@example.com',
    subject='Plain Text Message',
    body='This is a plain text email via Postmark.',
    html=False
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 3: Email with tracking
print("Example 3: Email with tracking (opens & links)")
response = mailer.send(
    to='recipient@example.com',
    subject='Tracked Email',
    body='<p>This email tracks opens and link clicks.</p><p><a href="https://example.com">Click here</a></p>',
    track_opens=True,  # Track email opens
    track_links='HtmlAndText'  # Track link clicks
)
print(f"✓ Sent with tracking! Message ID: {response.message_id}")
print()


# Example 4: Email with CC and BCC
print("Example 4: Email with CC and BCC")
response = mailer.send(
    to='recipient@example.com',
    subject='Project Update',
    body='<p>Latest project update...</p>',
    cc=['manager@example.com'],
    bcc=['admin@example.com']
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 5: Email with attachments
print("Example 5: Email with attachments")
from pathlib import Path

attachment_path = Path('document.pdf')
if attachment_path.exists():
    response = mailer.send(
        to='recipient@example.com',
        subject='Document Attached',
        body='<p>Please find the document attached.</p>',
        attachments=[attachment_path]
    )
    print(f"✓ Sent with attachment! Message ID: {response.message_id}")
else:
    print("⚠ Skipping attachment example (file not found)")
print()


# Example 6: Email with custom headers
print("Example 6: Email with custom headers")
response = mailer.send(
    to='recipient@example.com',
    subject='Newsletter',
    body='<p>Monthly newsletter...</p>',
    headers={
        'X-Campaign-ID': 'newsletter-nov-2024',
        'X-Priority': '1'
    }
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 7: Email with message stream (Postmark feature)
print("Example 7: Email with message stream")
mailer_transactional = MailBridge(
    provider='postmark',
    server_token='your-postmark-server-token',
    from_email='noreply@yourdomain.com',
    message_stream='outbound'  # or 'broadcasts' for marketing
)

response = mailer_transactional.send(
    to='recipient@example.com',
    subject='Order Confirmation',
    body='<p>Your order has been confirmed!</p>'
)
print(f"✓ Sent via message stream! Message ID: {response.message_id}")
print()


print("=" * 60)
print("All Postmark basic examples completed!")
print()
print("📝 Postmark Features:")
print("  • Excellent deliverability")
print("  • Open and click tracking")
print("  • Message streams (transactional vs broadcast)")
print("  • Bounce and spam complaint webhooks")
print("  • Detailed analytics")
print("=" * 60)