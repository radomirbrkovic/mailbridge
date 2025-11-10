"""
Amazon SES Provider - Bulk Email Example

This example shows how to send bulk emails using Amazon SES.
SES has a 50-recipient limit per call, which MailBridge handles automatically.
"""

from mailbridge import MailBridge
from mailbridge import EmailMessageDto
from mailbridge import BulkEmailDTO

# Initialize SES provider
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)

# Example 1: Simple bulk sending
print("Example 1: Simple bulk sending")
messages = [
    EmailMessageDto(
        to='user1@example.com',
        subject='Welcome',
        body='<p>Welcome User 1!</p>'
    ),
    EmailMessageDto(
        to='user2@example.com',
        subject='Welcome',
        body='<p>Welcome User 2!</p>'
    ),
    EmailMessageDto(
        to='user3@example.com',
        subject='Welcome',
        body='<p>Welcome User 3!</p>'
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Sent: {result.successful}/{result.total}")
print(f"✗ Failed: {result.failed}")
print()

# Example 2: Bulk template emails (recommended for SES)
print("Example 2: Bulk template emails")
messages = [
    EmailMessageDto(
        to='alice@example.com',
        template_id='WelcomeTemplate',
        template_data={'firstName': 'Alice', 'plan': 'Pro'}
    ),
    EmailMessageDto(
        to='bob@example.com',
        template_id='WelcomeTemplate',
        template_data={'firstName': 'Bob', 'plan': 'Enterprise'}
    ),
    EmailMessageDto(
        to='charlie@example.com',
        template_id='WelcomeTemplate',
        template_data={'firstName': 'Charlie', 'plan': 'Basic'}
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Template emails sent: {result.successful}/{result.total}")
print()

# Example 3: Large bulk send (auto-batched to 50 per call)
print("Example 3: Large bulk send with auto-batching")
print("  SES limit: 50 destinations per API call")
print("  MailBridge automatically batches for you!")

# Create 150 messages (will be sent in 3 batches of 50)
messages = []
for i in range(150):
    messages.append(
        EmailMessageDto(
            to=f'user{i}@example.com',
            template_id='BulkTemplate',
            template_data={
                'userId': str(i),
                'userName': f'User {i}'
            }
        )
    )

result = mailer.send_bulk(messages)
print(f"✓ Large bulk sent: {result.successful}/{result.total}")
print(f"  → Automatically batched into multiple API calls")
print()

# Example 4: Bulk with BulkEmailDTO
print("Example 4: Using BulkEmailDTO")
bulk = BulkEmailDTO(
    messages=[
        EmailMessageDto(
            to='user1@example.com',
            template_id='NewsletterTemplate',
            template_data={'month': 'November'}
        ),
        EmailMessageDto(
            to='user2@example.com',
            template_id='NewsletterTemplate',
            template_data={'month': 'November'}
        ),
    ],
    default_from='newsletter@yourdomain.com'
)

result = mailer.send_bulk(bulk)
print(f"✓ Sent: {result.successful}/{result.total}")
print()

# Example 5: Mixed template bulk
print("Example 5: Multiple different templates in bulk")
messages = [
    EmailMessageDto(
        to='newuser@example.com',
        template_id='WelcomeTemplate',
        template_data={'firstName': 'New User'}
    ),
    EmailMessageDto(
        to='premium@example.com',
        template_id='UpgradeTemplate',
        template_data={'plan': 'Premium'}
    ),
    EmailMessageDto(
        to='inactive@example.com',
        template_id='RetentionTemplate',
        template_data={'lastLogin': '30 days ago'}
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Mixed templates sent: {result.successful}/{result.total}")
print()

# Example 6: Bulk with error handling
print("Example 6: Bulk with error handling")
messages = [
    EmailMessageDto(
        to='valid1@example.com',
        template_id='TestTemplate',
        template_data={'name': 'Valid 1'}
    ),
    EmailMessageDto(
        to='invalid-email',  # Invalid email
        template_id='TestTemplate',
        template_data={'name': 'Invalid'}
    ),
    EmailMessageDto(
        to='valid2@example.com',
        template_id='TestTemplate',
        template_data={'name': 'Valid 2'}
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Successful: {result.successful}")
print(f"✗ Failed: {result.failed}")

if result.failures:
    print("\nFailure details:")
    for failure in result.failures:
        print(f"  - {failure.to}: {failure.error}")
print()

# Example 7: Bulk sending with configuration set
print("Example 7: Bulk with tracking")
mailer_tracked = MailBridge(
    provider='ses',
    aws_access_key_id='your-access-key-id',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1',
    from_email='verified@yourdomain.com',
    configuration_set_name='tracking-config'
)

messages = [
    EmailMessageDto(
        to=f'user{i}@example.com',
        template_id='CampaignTemplate',
        template_data={'userId': str(i), 'campaignId': 'bf-2024'}
    )
    for i in range(100)
]

result = mailer_tracked.send_bulk(messages)
print(f"✓ Tracked bulk sent: {result.successful}/{result.total}")
print("  → All emails tracked via configuration set")
print()

# Example 8: Check bulk support
print("Example 8: Check bulk sending support")
if mailer.supports_bulk_sending():
    print("✓ SES supports bulk sending!")
    print("  → Uses send_bulk_templated_email API")
    print("  → Automatically batches to 50 destinations")

    messages = [
        EmailMessageDto(
            to=f'user{i}@example.com',
            template_id='TestTemplate',
            template_data={'id': str(i)}
        )
        for i in range(75)  # Will be split into 2 batches
    ]

    result = mailer.send_bulk(messages)
    print(f"  → Sent {result.successful} emails in batched calls")
else:
    print("✗ Bulk not supported")
print()

# Example 9: Segmented bulk sending
print("Example 9: Segmented campaigns")

# Free tier users
free_segment = [
    EmailMessageDto(
        to=f'free{i}@example.com',
        template_id='FreeTierTemplate',
        template_data={'tier': 'Free', 'upgradeUrl': 'https://...'}
    )
    for i in range(50)
]

# Pro tier users
pro_segment = [
    EmailMessageDto(
        to=f'pro{i}@example.com',
        template_id='ProTierTemplate',
        template_data={'tier': 'Pro', 'features': 'Premium features'}
    )
    for i in range(30)
]

result1 = mailer.send_bulk(free_segment)
result2 = mailer.send_bulk(pro_segment)

print(f"✓ Free tier: {result1.successful}/{result1.total}")
print(f"✓ Pro tier: {result2.successful}/{result2.total}")
print()

print("=" * 60)
print("All Amazon SES bulk examples completed!")
print()
print("💡 SES Bulk Sending Tips:")
print("  • Use templates for better performance")
print("  • 50 destination limit per API call (auto-batched)")
print("  • send_bulk_templated_email is most efficient")
print("  • Monitor sending quotas and rates")
print("  • Use configuration sets for tracking")
print("  • Watch for bounces and complaints")
print()
print("📊 SES Quotas (default):")
print("  • Sending rate: 14 emails/second")
print("  • Daily sending quota: 200 emails/day (sandbox)")
print("  • Request production access for higher limits")
print("=" * 60)