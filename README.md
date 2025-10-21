# 📧 MailBridge

**MailBridge** is a flexible Python library for sending emails, allowing you to use multiple providers through a single, simple interface.
It supports **SMTP**, **SendGrid**, **Mailgun**, **Amazon SES**, **Postmark**, and **Brevo**.

The package uses the **Facade pattern**, so clients only need to call one method to send an email, while the provider implementation can be swapped via configuration.

## ⚡ Features
- Unified API for all email providers (`Mail.send(...)`)
- Support for: SMTP, SendGrid, Mailgun, Amazon SES, Postmark, Brevo
- Configurable via `.env` file
- Easy integration into any Python project
- Selective provider installation

## 🛠️ Tech Stack

- Python 3.10+
- `requests` for HTTP providers
- `boto3` for AWS SES
- Standard library `smtplib` for SMTP

## 📦 Installation

Install only the providers you need using **extras**:
```
# Only SMTP
pip install mailbridge[smtp]

# Only SES
pip install mailbridge[ses]

# Only SendGrid
pip install mailbridge[sendgrid]

# All providers
pip install mailbridge[all]
```

## ⚙️ Configuration

Create a `.env` file and define the variables for your chosen provider:

```
# Example for SMTP
MAIL_MAILER=smtp
MAIL_HOST=smtp.mailserver.com
MAIL_PORT=587
MAIL_USERNAME=your_username
MAIL_PASSWORD=your_password
MAIL_TLS_ENCRYPTION=True
MAIL_SSL_ENCRYPTION=False

# Example for SendGrid
MAIL_MAILER=sendgrid
MAIL_API_KEY=your_sendgrid_api_key
MAIL_ENDPOINT=https://api.sendgrid.com/v3/mail/send
```

## 🚀 Usage
### Sending an email:

```
from mailbridge import Mail

Mail.send(
    to="user@example.com",
    subject="Welcome!",
    body="<h1>Hello from MailBridge!</h1>",
    from_email="no-reply@example.com"
)
```

### Dynamically choosing a provider from `.env`:
- Change `MAIL_MAILER` in `.env` to `"smtp"`, `"sendgrid"`, `"mailgun"`, `"ses"`, `"postmark"` or `"brevo"`.
- MailBridge will automatically use the corresponding provider

## 📂 Project Structure

```
mailbridge/
├── mailbridge/
│   ├── __init__.py
│   ├── mail.py               # Facade
│   ├── mailer_factory.py     # MailerFactory
│   └── providers/
│       ├── provider_interface.py
│       ├── smtp_provider.py
│       ├── sendgrid_provider.py
│       ├── mailgun_provider.py
│       ├── ses_provider.py
│       ├── postmark_provider.py
│       └── brevo_provider.py
├── tests/
├── setup.py
├── pyproject.toml
└── README.md
```

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/license/MIT).