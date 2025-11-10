"""
SendGrid Provider - Bulk Email Example

This example shows how to send bulk emails efficiently using SendGrid.
SendGrid has a native bulk API that MailBridge uses automatically.
"""

from mailbridge import MailBridge
from mailbridge import EmailMessageDto
from mailbridge import BulkEmailDTO

# Initialize SendGrid provider
mailer = MailBridge(
    provider='sendgrid',
    api_key='your-sendgrid-api-key',
    from_email='noreply@yourcompany.com'
)

# Example 1: Simple bulk sending
print("Example 1: Simple bulk sending")
messages = [
    EmailMessageDto(
        to='user1@example.com',
        subject='Welcome User 1',
        body='<p>Hello User 1!</p>'
    ),
    EmailMessageDto(
        to='user2@example.com',
        subject='Welcome User 2',
        body='<p>Hello User 2!</p>'
    ),
    EmailMessageDto(
        to='user3@example.com',
        subject='Welcome User 3',
        body='<p>Hello User 3!</p>'
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Sent: {result.successful}/{result.total}")
print(f"✗ Failed: {result.failed}")
print()

# Example 2: Bulk sending with shared defaults
print("Example 2: Bulk with default from")
messages = [
    EmailMessageDto(to='user1@example.com', subject='Update', body='<p>News 1</p>'),
    EmailMessageDto(to='user2@example.com', subject='Update', body='<p>News 2</p>'),
    EmailMessageDto(to='user3@example.com', subject='Update', body='<p>News 3</p>'),
]

result = mailer.send_bulk(
    messages,
    default_from='newsletter@yourcompany.com',
    tags=['newsletter', 'november-2024']
)
print(f"✓ Newsletter sent: {result.successful}/{result.total}")
print()

# Example 3: Bulk template emails (personalized for each recipient)
print("Example 3: Bulk template emails with personalization")
messages = [
    EmailMessageDto(
        to='alice@example.com',
        subject='',
        body='',
        template_id='d-welcome-template',
        template_data={'name': 'Alice', 'plan': 'Pro'}
    ),
    EmailMessageDto(
        to='bob@example.com',
        subject='',
        body='',
        template_id='d-welcome-template',
        template_data={'name': 'Bob', 'plan': 'Enterprise'}
    ),
    EmailMessageDto(
        to='charlie@example.com',
        subject='',
        body='',
        template_id='d-welcome-template',
        template_data={'name': 'Charlie', 'plan': 'Basic'}
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Personalized templates sent: {result.successful}/{result.total}")
print()

# Example 4: Large bulk send (automatic batching)
print("Example 4: Large bulk send (1000 emails)")
messages = []
for i in range(1000):
    messages.append(
        EmailMessageDto(
            to=f'user{i}@example.com',
            subject=f'Bulk Email {i}',
            body=f'<p>This is bulk email number {i}</p>'
        )
    )

# SendGrid will handle this efficiently with native bulk API
result = mailer.send_bulk(messages)
print(f"✓ Bulk sent: {result.successful}/{result.total}")
print(f"  Time taken: {result.total_time:.2f}s" if hasattr(result, 'total_time') else "")
print()

# Example 5: Bulk with BulkEmailDTO (explicit configuration)
print("Example 5: Using BulkEmailDTO")
bulk = BulkEmailDTO(
    messages=[
        EmailMessageDto(to='user1@example.com', subject='Test', body='Body 1'),
        EmailMessageDto(to='user2@example.com', subject='Test', body='Body 2'),
        EmailMessageDto(to='user3@example.com', subject='Test', body='Body 3'),
    ],
    default_from='bulk@yourcompany.com',
    tags=['test-campaign']
)

result = mailer.send_bulk(bulk)
print(f"✓ Sent: {result.successful}/{result.total}")
print()

# Example 6: Mixed template bulk (different templates)
print("Example 6: Mixed templates in bulk")
messages = [
    EmailMessageDto(
        to='newuser@example.com',
        template_id='d-welcome-template',
        template_data={'name': 'New User'}
    ),
    EmailMessageDto(
        to='premium@example.com',
        template_id='d-upgrade-template',
        template_data={'plan': 'Premium', 'discount': '20%'}
    ),
    EmailMessageDto(
        to='churning@example.com',
        template_id='d-retention-template',
        template_data={'offer': 'Stay with us!'}
    ),
]

result = mailer.send_bulk(messages)
print(f"✓ Mixed templates sent: {result.successful}/{result.total}")
print()

# Example 7: Bulk with error handling
print("Example 7: Bulk with error handling")
messages = [
    EmailMessageDto(to='valid1@example.com', subject='Test', body='Body 1'),
    EmailMessageDto(to='invalid-email', subject='Test', body='Body 2'),  # Invalid
    EmailMessageDto(to='valid2@example.com', subject='Test', body='Body 3'),
]

result = mailer.send_bulk(messages)
print(f"✓ Successful: {result.successful}")
print(f"✗ Failed: {result.failed}")

if result.failures:
    print("\nFailure details:")
    for failure in result.failures:
        print(f"  - {failure.to}: {failure.error}")
print()

# Example 8: Check bulk sending support
print("Example 8: Check if bulk is supported")
if mailer.supports_bulk_sending():
    print("✓ SendGrid supports native bulk sending!")
    print("  → Uses SendGrid's batch API for efficiency")

    messages = [EmailMessageDto(to=f'user{i}@example.com', subject='Test', body='Body')
                for i in range(100)]
    result = mailer.send_bulk(messages)
    print(f"  → Sent {result.successful} emails efficiently")
else:
    print("✗ Provider doesn't support bulk (will send individually)")
print()

# Example 9: Segmented bulk sending
print("Example 9: Segmented bulk sending")

# Segment 1: Free users
free_users = [
    EmailMessageDto(
        to=f'free{i}@example.com',
        template_id='d-free-tier-template',
        template_data={'tier': 'Free', 'upgrade_link': 'https://...'}
    )
    for i in range(50)
]

# Segment 2: Pro users
pro_users = [
    EmailMessageDto(
        to=f'pro{i}@example.com',
        template_id='d-pro-tier-template',
        template_data={'tier': 'Pro', 'features': ['Feature A', 'Feature B']}
    )
    for i in range(30)
]

# Send each segment
result1 = mailer.send_bulk(free_users, tags=['segment-free', 'campaign-2024'])
result2 = mailer.send_bulk(pro_users, tags=['segment-pro', 'campaign-2024'])

print(f"✓ Free tier: {result1.successful}/{result1.total}")
print(f"✓ Pro tier: {result2.successful}/{result2.total}")
print()

print("=" * 60)
print("All SendGrid bulk examples completed!")
print()
print("💡 Tips:")
print("  • SendGrid uses native batch API (efficient)")
print("  • Can send up to 1000 emails per API call")
print("  • Each recipient can have personalized data")
print("  • Supports template personalization at scale")
print("=" * 60)