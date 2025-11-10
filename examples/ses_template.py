"""
Amazon SES Provider - Template Email Example

This example shows how to send template emails using Amazon SES.
Templates must be created in SES console first.
"""

from mailbridge import MailBridge

# Initialize SES provider
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)

# Example 1: Basic template email
print("Example 1: Basic template email")
response = mailer.send(
    to='user@example.com',
    subject='',  # Subject from template
    body='',  # Body from template
    template_id='WelcomeTemplate',  # Your SES template name
    template_data={
        'firstName': 'John',
        'lastName': 'Doe',
        'activationUrl': 'https://yourapp.com/activate/abc123'
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
    template_id='WelcomeTemplate',
    template_data={
        'firstName': 'Alice',
        'companyName': 'Acme Corp',
        'supportEmail': 'support@yourdomain.com',
        'year': '2024'
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
    template_id='PasswordResetTemplate',
    template_data={
        'userName': 'Bob Johnson',
        'resetUrl': 'https://yourapp.com/reset?token=xyz789',
        'expiryHours': '24'
    }
)
print(f"✓ Password reset email sent! Message ID: {response.message_id}")
print()

# Example 4: Invoice template with nested data
print("Example 4: Invoice template")
response = mailer.send(
    to='customer@example.com',
    subject='',
    body='',
    template_id='InvoiceTemplate',
    template_data={
        'customerName': 'Jane Wilson',
        'invoiceNumber': 'INV-2024-001',
        'totalAmount': '299.00',
        'currency': 'USD',
        'dueDate': '2024-12-31',
        'lineItems': [
            {'description': 'Pro Plan', 'quantity': '1', 'price': '199.00'},
            {'description': 'Extra Storage', 'quantity': '2', 'price': '50.00'}
        ]
    }
)
print(f"✓ Invoice email sent! Message ID: {response.message_id}")
print()

# Example 5: Template with default values
print("Example 5: Template with default values")
response = mailer.send(
    to='user@example.com',
    subject='',
    body='',
    template_id='NewsletterTemplate',
    template_data={
        'month': 'November',
        'year': '2024',
        # Some values may have defaults in template
    }
)
print(f"✓ Newsletter sent! Message ID: {response.message_id}")
print()

# Example 6: Check template support
print("Example 6: Check template support")
if mailer.supports_templates():
    print("✓ Amazon SES supports templates!")

    response = mailer.send(
        to='user@example.com',
        subject='',
        body='',
        template_id='MyTemplate',
        template_data={'key': 'value'}
    )
    print(f"✓ Template sent! Message ID: {response.message_id}")
else:
    print("✗ Templates not supported")
print()

# Example 7: Template with configuration set (tracking)
print("Example 7: Template with tracking")
mailer_tracked = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',
    from_email='verified@yourdomain.com',
    configuration_set_name='tracking-config'
)

response = mailer_tracked.send(
    to='user@example.com',
    subject='',
    body='',
    template_id='MarketingTemplate',
    template_data={
        'campaignId': 'bf-2024',
        'offerCode': 'SAVE20'
    }
)
print(f"✓ Tracked template email sent! Message ID: {response.message_id}")
print()

print("=" * 60)
print("All Amazon SES template examples completed!")
print()
print("📝 How to create SES templates:")
print("  1. AWS Console → Amazon SES → Email Templates")
print("  2. Click 'Create Template'")
print("  3. Define template with {{variables}}")
print()
print("Example template (JSON):")
print("""
{
  "TemplateName": "WelcomeTemplate",
  "SubjectPart": "Welcome {{firstName}}!",
  "HtmlPart": "<h1>Hello {{firstName}} {{lastName}}!</h1>",
  "TextPart": "Hello {{firstName}} {{lastName}}!"
}
""")
print()
print("Or use AWS CLI:")
print("  aws ses create-template --cli-input-json file://template.json")
print("=" * 60)