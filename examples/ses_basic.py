"""
Amazon SES Provider - Basic Email Example

This example shows how to send basic emails using Amazon SES.
"""

from mailbridge import MailBridge

# Initialize SES provider
# Option 1: Using AWS credentials
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',  # Your AWS region
    from_email='verified@yourdomain.com'  # Must be verified in SES
)

# Option 2: Using IAM role (if running on EC2/Lambda)
# mailer = MailBridge(
#     provider='ses',
#     region_name='us-east-1',
#     from_email='verified@yourdomain.com'
# )


# Example 1: Simple email
print("Example 1: Simple HTML email")
response = mailer.send(
    to='recipient@example.com',
    subject='Welcome to Our Service',
    body='<h1>Hello from SES!</h1><p>This is an HTML email.</p>',
    html=True
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 2: Plain text email
print("Example 2: Plain text email")
response = mailer.send(
    to='recipient@example.com',
    subject='Plain Text Message',
    body='This is a plain text email sent via Amazon SES.',
    html=False
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 3: Email with CC and BCC
print("Example 3: Email with CC and BCC")
response = mailer.send(
    to='recipient@example.com',
    subject='Project Update',
    body='<p>Here is the latest project update...</p>',
    cc=['manager@example.com'],
    bcc=['admin@example.com']
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 4: Email with Reply-To
print("Example 4: Email with Reply-To")
response = mailer.send(
    to='recipient@example.com',
    subject='Customer Support',
    body='<p>We received your inquiry. Reply to this email for assistance.</p>',
    reply_to='support@yourdomain.com'
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 5: Email with attachments
print("Example 5: Email with attachments")
from pathlib import Path

attachment_path = Path('report.pdf')
if attachment_path.exists():
    response = mailer.send(
        to='recipient@example.com',
        subject='Monthly Report',
        body='<p>Please find the monthly report attached.</p>',
        attachments=[attachment_path]
    )
    print(f"✓ Sent with attachment! Message ID: {response.message_id}")
    print("  Note: SES uses send_raw_email for attachments")
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
    body='<h2>Important Update</h2><p>Please review this information.</p>'
)
print(f"✓ Sent to multiple recipients! Message ID: {response.message_id}")
print()


# Example 7: Email with custom headers
print("Example 7: Email with custom headers")
response = mailer.send(
    to='recipient@example.com',
    subject='Newsletter',
    body='<p>Our monthly newsletter...</p>',
    headers={
        'X-Campaign-ID': 'newsletter-nov-2024',
        'X-Priority': '3'
    }
)
print(f"✓ Sent! Message ID: {response.message_id}")
print()


# Example 8: Using configuration set (for tracking)
print("Example 8: Using configuration set")
mailer_with_tracking = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',
    from_email='verified@yourdomain.com',
    configuration_set_name='my-tracking-set'  # Optional: for open/click tracking
)

response = mailer_with_tracking.send(
    to='recipient@example.com',
    subject='Tracked Email',
    body='<p>This email is being tracked via SES configuration set.</p>'
)
print(f"✓ Sent with tracking! Message ID: {response.message_id}")
print()


print("=" * 60)
print("All Amazon SES basic examples completed!")
print()
print("📝 Important Notes:")
print("  • Email addresses must be verified in SES (sandbox mode)")
print("  • Move out of sandbox to send to any email")
print("  • Verify domains for better deliverability")
print("  • Use configuration sets for tracking")
print("  • Monitor bounce/complaint rates")
print("=" * 60)