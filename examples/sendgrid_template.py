"""
SendGrid Provider - Template Email Example

This example shows how to send template emails using SendGrid.
You need to create templates in SendGrid dashboard first.
"""

from mailbridge import MailBridge

# Initialize SendGrid provider
mailer = MailBridge(
    provider='sendgrid',
    api_key='your-sendgrid-api-key',
    from_email='noreply@yourcompany.com'
)

# Example 1: Basic template email
print("Example 1: Basic template email")
response = mailer.send(
    to='user@example.com',
    subject='',  # Subject from template
    body='',  # Body from template
    template_id='d-1234567890abcdef',  # Your SendGrid template ID
    template_data={
        'first_name': 'John',
        'last_name': 'Doe',
        'company': 'Acme Corp'
    }
)
print(f"✓ Template email sent! Message ID: {response.message_id}")
print()

# Example 2: Welcome email template
print("Example 2: Welcome email template")
response = mailer.send(
    to='newuser@example.com',
    subject='',
    body='',
    template_id='d-welcome-template',
    template_data={
        'user_name': 'Alice Smith',
        'activation_link': 'https://yourapp.com/activate/abc123',
        'support_email': 'support@yourcompany.com'
    }
)
print(f"✓ Welcome email sent! Message ID: {response.message_id}")
print()

# Example 3: Password reset template
print("Example 3: Password reset template")
response = mailer.send(
    to='user@example.com',
    subject='',
    body='',
    template_id='d-password-reset',
    template_data={
        'user_name': 'Bob Johnson',
        'reset_link': 'https://yourapp.com/reset/xyz789',
        'expiry_time': '24 hours'
    }
)
print(f"✓ Password reset email sent! Message ID: {response.message_id}")
print()

# Example 4: Invoice template with dynamic data
print("Example 4: Invoice template")
response = mailer.send(
    to='customer@example.com',
    subject='',
    body='',
    template_id='d-invoice-template',
    template_data={
        'customer_name': 'Jane Wilson',
        'invoice_number': 'INV-2024-001',
        'amount': '$299.00',
        'due_date': '2024-12-31',
        'items': [
            {'name': 'Pro Plan', 'quantity': 1, 'price': '$199.00'},
            {'name': 'Extra Storage', 'quantity': 2, 'price': '$50.00'}
        ]
    }
)
print(f"✓ Invoice email sent! Message ID: {response.message_id}")
print()

# Example 5: Template with multiple recipients (personalization)
print("Example 5: Multiple recipients with different data")
from mailbridge.dto.email_message_dto import EmailMessageDto

# Note: For true personalization, use bulk sending
# This is just showing template with multiple recipients
response = mailer.send(
    to=['user1@example.com', 'user2@example.com'],
    subject='',
    body='',
    template_id='d-newsletter-template',
    template_data={
        'month': 'November',
        'year': '2024',
        'headline': 'Our Biggest Update Yet!'
    }
)
print(f"✓ Newsletter sent to multiple recipients! Message ID: {response.message_id}")
print()

# Example 6: Template with custom headers and tags
print("Example 6: Template with tracking")
response = mailer.send(
    to='user@example.com',
    subject='',
    body='',
    template_id='d-marketing-template',
    template_data={
        'first_name': 'Chris',
        'offer_code': 'SAVE20',
        'offer_expiry': '2024-12-15'
    },
    tags=['marketing', 'black-friday', '2024'],
    headers={
        'X-Campaign-ID': 'bf-2024',
        'X-Segment': 'premium-users'
    }
)
print(f"✓ Marketing email sent with tracking! Message ID: {response.message_id}")
print()

# Example 7: Check if provider supports templates
print("Example 7: Check template support")
if mailer.supports_templates():
    print("✓ SendGrid supports templates!")

    response = mailer.send(
        to='user@example.com',
        subject='',
        body='',
        template_id='d-any-template',
        template_data={'key': 'value'}
    )
    print(f"✓ Template sent! Message ID: {response.message_id}")
else:
    print("✗ Templates not supported")
print()

print("=" * 60)
print("All SendGrid template examples completed!")
print()
print("📝 Note: You need to create templates in SendGrid dashboard first:")
print("   1. Go to https://app.sendgrid.com/")
print("   2. Navigate to Email API → Dynamic Templates")
print("   3. Create a template and note the template ID")
print("   4. Use the template ID (starts with 'd-') in your code")
print("=" * 60)