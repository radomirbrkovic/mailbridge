# MailBridge Examples 📚

Comprehensive examples for all MailBridge providers.

## 📁 Available Examples

### SendGrid
- **`sendgrid_basic.py`** - Basic email sending (HTML, plain text, CC/BCC, attachments)
- **`sendgrid_template.py`** - Template emails with dynamic data
- **`sendgrid_bulk.py`** - Bulk sending with native batch API

### Amazon SES
- **`ses_basic.py`** - Basic email sending with AWS credentials
- **`ses_template.py`** - Template emails (must create templates in AWS)
- **`ses_bulk.py`** - Bulk sending with automatic 50-recipient batching

### Postmark
- **`postmark_basic.py`** - Basic emails with tracking options

### SMTP
- **`smtp_basic.py`** - Generic SMTP (Gmail, Outlook, custom servers)

---

## 🚀 Quick Start

### 1. Install MailBridge

```bash
pip install mailbridge
```

### 2. Choose Your Provider

```python
from mailbridge import MailBridge

# SendGrid
mailer = MailBridge(provider='sendgrid', api_key='your-key')

# Amazon SES
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='your-key',
    aws_secret_access_key='your-secret',
    region_name='us-east-1'
)

# Postmark
mailer = MailBridge(provider='postmark', server_token='your-token')

# SMTP
mailer = MailBridge(
    provider='smtp',
    host='smtp.gmail.com',
    port=587,
    username='you@gmail.com',
    password='your-app-password',
    use_tls=True
)
```

### 3. Send Email

```python
# Simple email
response = mailer.send(
    to='recipient@example.com',
    subject='Hello',
    body='<h1>Hello World!</h1>'
)
print(f"Sent! Message ID: {response.message_id}")

# Template email (SendGrid, SES, Postmark)
response = mailer.send(
    to='user@example.com',
    subject='',
    body='',
    template_id='your-template-id',
    template_data={'name': 'John', 'company': 'Acme'}
)

# Bulk sending
from mailbridge.dto.email_message_dto import EmailMessageDto

messages = [
    EmailMessageDto(to='user1@example.com', subject='Hi', body='Hello 1'),
    EmailMessageDto(to='user2@example.com', subject='Hi', body='Hello 2'),
]

result = mailer.send_bulk(messages)
print(f"Sent: {result.successful}/{result.total}")
```

---

## 📖 Example Categories

### Basic Features
- HTML and plain text emails
- CC, BCC, Reply-To
- Custom headers
- Attachments
- Multiple recipients

### Advanced Features
- **Templates** (SendGrid, SES, Postmark)
- **Bulk sending** (all providers)
- **Tracking** (Postmark)
- **Configuration sets** (SES)
- **Message streams** (Postmark)

### Provider-Specific
- **SendGrid**: Native batch API, personalizations
- **SES**: 50-recipient batching, IAM roles
- **Postmark**: Open/click tracking, message streams
- **SMTP**: TLS/SSL, Gmail app passwords

---

## 🔧 Configuration Examples

### SendGrid

```python
mailer = MailBridge(
    provider='sendgrid',
    api_key='SG.xxxx',
    from_email='noreply@yourdomain.com'  # Optional default
)
```

### Amazon SES

```python
# With credentials
mailer = MailBridge(
    provider='ses',
    aws_access_key_id='AKIAXXXX',
    aws_secret_access_key='xxxx',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)

# With IAM role (EC2/Lambda)
mailer = MailBridge(
    provider='ses',
    region_name='us-east-1',
    from_email='verified@yourdomain.com'
)

# With configuration set (tracking)
mailer = MailBridge(
    provider='ses',
    region_name='us-east-1',
    configuration_set_name='tracking-config'
)
```

### Postmark

```python
mailer = MailBridge(
    provider='postmark',
    server_token='xxxx-xxxx-xxxx',
    from_email='verified@yourdomain.com',
    message_stream='outbound'  # or 'broadcasts'
)
```

### SMTP

```python
# Gmail
mailer = MailBridge(
    provider='smtp',
    host='smtp.gmail.com',
    port=587,
    username='you@gmail.com',
    password='app-password',  # Not regular password!
    use_tls=True
)

# Outlook
mailer = MailBridge(
    provider='smtp',
    host='smtp.office365.com',
    port=587,
    username='you@outlook.com',
    password='password',
    use_tls=True
)

# Custom with SSL
mailer = MailBridge(
    provider='smtp',
    host='mail.yourdomain.com',
    port=465,
    username='user',
    password='pass',
    use_ssl=True
)
```

---

## 💡 Best Practices

### For Production

1. **Use environment variables** for credentials
   ```python
   import os
   
   mailer = MailBridge(
       provider='sendgrid',
       api_key=os.getenv('SENDGRID_API_KEY')
   )
   ```

2. **Use templates** for better maintainability
   ```python
   # Better than hardcoded HTML
   mailer.send(
       to='user@example.com',
       template_id='welcome-email',
       template_data={'name': user.name}
   )
   ```

3. **Handle errors gracefully**
   ```python
   try:
       response = mailer.send(...)
       if response.success:
           print(f"Sent: {response.message_id}")
   except EmailSendError as e:
       logger.error(f"Failed to send: {e}")
   ```

4. **Use bulk sending** for multiple emails
   ```python
   # More efficient than loop
   result = mailer.send_bulk(messages)
   ```

5. **Close connections** when done
   ```python
   with MailBridge(provider='smtp', ...) as mailer:
       mailer.send(...)
   # Auto-closed
   ```

### For Each Provider

**SendGrid:**
- Use native bulk API for >10 emails
- Add tags for tracking campaigns
- Use personalizations for individual data

**SES:**
- Verify sender domains in production
- Use configuration sets for tracking
- Monitor bounce rates
- Templates are more efficient than regular bulk

**Postmark:**
- Enable tracking for analytics
- Use message streams to separate transactional/marketing
- Monitor deliverability reports

**SMTP:**
- Use App Passwords for Gmail/Outlook
- Implement retry logic for transient failures
- Consider rate limiting for bulk sends

---

## 🔗 Resources

### Documentation
- [MailBridge Docs](https://github.com/yourusername/mailbridge)
- [SendGrid API](https://docs.sendgrid.com/)
- [Amazon SES API](https://docs.aws.amazon.com/ses/)
- [Postmark API](https://postmarkapp.com/developer)

### Tutorials
- Creating email templates
- Setting up SPF/DKIM
- Monitoring deliverability
- Handling bounces and complaints

### Support
- GitHub Issues: [issues](https://github.com/yourusername/mailbridge/issues)
- Email: support@mailbridge.dev

---

## 📝 Running Examples

```bash
# Clone repo
git clone https://github.com/yourusername/mailbridge
cd mailbridge/examples

# Install dependencies
pip install mailbridge

# Update credentials in example files
# Then run
python sendgrid_basic.py
python ses_template.py
python postmark_basic.py
```

---

## ⚠️ Important Notes

### Gmail SMTP
- **Must use App Password**, not regular password
- Enable 2FA first
- Generate App Password in Google Account settings

### Amazon SES
- **Verify email addresses** in sandbox mode
- **Request production access** to send to anyone
- Verify domains for better deliverability

### SendGrid
- **Free tier**: 100 emails/day
- API key format: `SG.xxxxx`
- Create in Settings → API Keys

### Postmark
- **Free trial**: 100 emails
- Verify sender signature or domain
- Excellent deliverability

---

## 🎯 Next Steps

1. Choose your provider
2. Copy example code
3. Update credentials
4. Run and test
5. Integrate into your app!

**Happy emailing! 📧**