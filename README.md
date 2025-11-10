# MailBridge 📧

**Unified Python email library with multi-provider support**

**MailBridge** is a flexible Python library for sending emails, allowing you to use multiple providers through a single, simple interface.
It supports **SMTP**, **SendGrid**, **Mailgun**, **Amazon SES**, **Postmark**, and **Brevo**.

---

## ✨ Features

- 🎨 **Template Support** - Use dynamic templates with all major providers
- 📎 **Attachment Support** - Add file attachment in email message
- 📦 **Bulk Sending** - Send thousands of emails efficiently with native API optimization
- 🔧 **Unified Interface** - Same code works with any provider
- ✅ **Fully Tested** - 156 unit tests, 96% coverage
- 🚀 **Production Ready** - Battle-tested and reliable
- 📚 **Great Documentation** - Extensive examples and guides

---

## 📦 Installation

```bash
pip install mailbridge
```

**Optional dependencies:**
```bash
# For SendGrid
pip install mailbridge[sendgrid]

# For Amazon SES
pip install mailbridge[ses]

# For all providers
pip install mailbridge[all]

# SMTP and Postmark work out of the box
```

---

## 🚀 Quick Start

### Basic Email

```python
from mailbridge import MailBridge

# Initialize with your provider
mailer = MailBridge(provider='sendgrid', api_key='your-api-key')

# Send email
response = mailer.send(
    to='recipient@example.com',
    subject='Hello from MailBridge!',
    body='<h1>It works!</h1><p>Email sent successfully.</p>'
)

print(f"Sent! Message ID: {response.message_id}")
```

### Template Email

```python
# Send template with dynamic data
response = mailer.send(
    to='user@example.com',
    subject='',  # From template
    body='',     # From template
    template_id='welcome-template',
    template_data={
        'name': 'John Doe',
        'company': 'Acme Corp',
        'activation_link': 'https://...'
    }
)
```

### Bulk Sending

```python
from mailbridge import MailBridge, EmailMessageDto

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
    # ... more messages
]

result = mailer.send_bulk(messages)
print(f"Sent: {result.successful}/{result.total}")
```

---

## 🎯 Supported Providers

| Provider | Templates | Bulk API | Features |
|----------|-----------|----------|----------|
| **SendGrid** | ✅ | ✅ Native | Personalizations, tracking |
| **Amazon SES** | ✅ | ✅ Native | 50/call batching, config sets |
| **Postmark** | ✅ | ✅ Native | Open/click tracking, streams |
| **Mailgun** | ✅ | ✅ Native | Templates, tracking |
| **Brevo** | ✅ | ✅ Native | Templates, SMS support |
| **SMTP** | ❌ | ❌ | Universal compatibility |

---

## 📖 Provider Setup

### SendGrid

```python
from mailbridge import MailBridge

mailer = MailBridge(
    provider='sendgrid',
    api_key='SG.xxxxx',
    from_email='noreply@yourdomain.com'
)
```

- [Get API Key](https://app.sendgrid.com/settings/api_keys)
- [Documentation](https://docs.sendgrid.com/)
- [Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/sengrid_basic.py)

---

### Amazon SES

```python
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='AKIAXXXX',
    aws_secret_access_key='xxxxx',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)

# Or using IAM role (EC2/Lambda)
mailer = MailBridge(
    provider='ses',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)
```

- [SES Console](https://console.aws.amazon.com/ses/)
- [Documentation](https://docs.aws.amazon.com/ses/)
- [Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/ses_basic.py)

**Note:** Email addresses must be verified in sandbox mode. Request production access to send to any email.

---

### Postmark

```python
mailer = MailBridge(
    provider='postmark',
    server_token='xxxxx-xxxxx',
    from_email='verified@yourdomain.com'
)

# With tracking
response = mailer.send(
    to='user@example.com',
    subject='Tracked Email',
    body='<p>Click <a href="https://...">here</a></p>',
    track_opens=True,
    track_links='HtmlAndText'
)
```

- [Get Token](https://account.postmarkapp.com/servers)
- [Documentation](https://postmarkapp.com/developer)
- [Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/postmark_basic.py)

---

### Mailgun

```python
mailer = MailBridge(
    provider='mailgun',
    api_key='key-xxxxx',
    domain='mg.yourdomain.com',  # Required
    from_email='noreply@yourdomain.com'
)
```

- [Get API Key](https://app.mailgun.com/settings/api_security)
- [Documentation](https://documentation.mailgun.com/)

**Note:** Uses same API as SendGrid. See [SendGrid examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/sendgrid_basic.py) for usage patterns.

---

### Brevo (Sendinblue)

```python
mailer = MailBridge(
    provider='brevo',
    api_key='xkeysib-xxxxx',
    from_email='noreply@yourdomain.com'
)

# Template ID is a number
mailer.send(
    to='user@example.com',
    template_id=123,  # Not a string
    template_data={'name': 'John'}
)
```

- [Get API Key](https://app.brevo.com/settings/keys/api)
- [Documentation](https://developers.brevo.com/)

**Note:** Similar to SendGrid/Postmark. Template IDs are integers. See [SendGrid examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/sendgrid_basic.py) for usage patterns.

---

### SMTP (Gmail, Outlook, Custom)

```python
# Gmail
mailer = MailBridge(
    provider='smtp',
    host='smtp.gmail.com',
    port=587,
    username='you@gmail.com',
    password='app-password',  # Not your regular password!
    use_tls=True,
    from_email='you@gmail.com'
)

# Outlook
mailer = MailBridge(
    provider='smtp',
    host='smtp.office365.com',
    port=587,
    username='you@outlook.com',
    password='your-password',
    use_tls=True,
    from_email='you@outlook.com'
)

# Custom server
mailer = MailBridge(
    provider='smtp',
    host='mail.yourdomain.com',
    port=465,
    username='user',
    password='pass',
    use_ssl=True,  # For port 465
    from_email='noreply@yourdomain.com'
)
```

- [Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/smtp_basic.py)

**Gmail:** Use [App Password](https://support.google.com/accounts/answer/185833) (requires 2FA)

---

## 💡 Common Use Cases

### Welcome Emails

```python
mailer.send(
    to=new_user.email,
    template_id='welcome-email',
    template_data={
        'name': new_user.name,
        'activation_link': generate_activation_link(new_user)
    }
)
```

### Password Reset

```python
mailer.send(
    to=user.email,
    template_id='password-reset',
    template_data={
        'reset_link': generate_reset_link(user),
        'expiry_hours': 24
    }
)
```

### Newsletters (Bulk)

```python
from mailbridge import EmailMessageDto

subscribers = User.objects.filter(subscribed=True)

messages = [
    EmailMessageDto(
        to=sub.email,
        template_id='newsletter',
        template_data={
            'name': sub.name,
            'unsubscribe_link': generate_unsubscribe_link(sub)
        }
    )
    for sub in subscribers
]

result = mailer.send_bulk(messages)
print(f"Sent: {result.successful}/{result.total}")
```

### Transactional Notifications

```python
mailer.send(
    to=order.customer_email,
    template_id='order-confirmation',
    template_data={
        'order_number': order.id,
        'total': order.total,
        'items': order.items,
        'tracking_url': order.tracking_url
    }
)
```

---

## 🔧 Advanced Features

### Attachments

```python
from pathlib import Path

mailer.send(
    to='customer@example.com',
    subject='Your Invoice',
    body='<p>Invoice attached.</p>',
    attachments=[
        Path('invoice.pdf'),
        Path('receipt.pdf')
    ]
)
```

### CC and BCC

```python
mailer.send(
    to='client@example.com',
    subject='Project Update',
    body='<p>Latest update...</p>',
    cc=['manager@company.com', 'team@company.com'],
    bcc=['archive@company.com']
)
```

### Custom Headers and Tags

```python
mailer.send(
    to='user@example.com',
    subject='Campaign Email',
    body='<p>Special offer!</p>',
    headers={'X-Campaign-ID': 'summer-2024'},
    tags=['marketing', 'campaign']
)
```

### Context Manager

```python
with MailBridge(provider='smtp', host='...', port=587) as mailer:
    mailer.send(to='user@example.com', subject='Test', body='...')
# Connection automatically closed
```

---

## 📊 Bulk Sending Performance

**Provider Optimizations:**

- **SendGrid**: Uses native batch API (up to 1000/call)
- **SES**: Auto-batches to 50 recipients per call
- **Postmark**: Uses batch API (up to 500/call)
- **Mailgun**: Native batch API
- **Brevo**: Native batch API
- **SMTP**: Reuses connection for multiple sends

**Example:**

```python
# Send 1000 emails efficiently
messages = [
    EmailMessageDto(
        to=f'user{i}@example.com',
        template_id='campaign',
        template_data={'user_id': i}
    )
    for i in range(1000)
]

result = mailer.send_bulk(messages)
print(f"Sent {result.successful} in {result.total_time:.2f}s")
```

---

## 📚 Documentation & Examples

- **[Examples Directory](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/)** - Complete examples for all providers
  - [SendGrid Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/sendgrid_basic.py) - Basic, template, bulk
  - [SES Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/ses_basic.py) - AWS setup, templates, bulk
  - [Postmark Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/postmark_basic.py) - Tracking features
  - [SMTP Examples](https://github.com/radomirbrkovic/mailbridge/blob/main/examples/smtp_basic.py) - Gmail, Outlook, custom
- **[Test Suite](https://github.com/radomirbrkovic/mailbridge/blob/main/tests/)** - 156 unit tests, 96% coverage
- **[Changelog](https://github.com/radomirbrkovic/mailbridge/blob/main/CHANGELOG.md)** - Version history

---

## 🧪 Testing

MailBridge includes a comprehensive test suite:

```bash
# Clone repo
git clone https://github.com/radomirbrkovic/mailbridge
cd mailbridge

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=mailbridge --cov-report=html

# Results: 156 tests, 96% coverage
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Setup development environment
git clone https://github.com/radomirbrkovic/mailbridge
cd mailbridge
pip install -e ".[dev]"

# Run tests
pytest

```

---

## 📄 License

MIT License - see [LICENSE](https://opensource.org/license/MIT) file for details.

---

## 🙏 Acknowledgments

Built with ❤️ for developers who need reliable email delivery.

**Credits:**
- SendGrid Python SDK
- Boto3 (AWS SDK)
- Postmark API
- Python SMTP library

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/radomirbrkovic/mailbridge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/radomirbrkovic/mailbridge/discussions)

---
