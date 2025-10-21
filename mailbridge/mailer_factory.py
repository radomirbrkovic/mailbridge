import os
from .providers.smtp_provider import SMTPProvider
from .providers.sendgrid_provider import SendGridProvider
from .providers.mailgun_provider import MailgunProvider
from .providers.ses_provider import SESProvider
from .providers.postmark_provider import PostmarkProvider
from .providers.brevo_provider import BrevoProvider
from dotenv import load_dotenv

load_dotenv()

class MailerFactory:
    @staticmethod
    def get_provider():
        provider_name = os.getenv("MAIL_MAILER", "smtp").lower()

        if provider_name == "smtp":
            return SMTPProvider(
                host=os.getenv("MAIL_HOST"),
                port=int(os.getenv("MAIL_PORT", 587)),
                username=os.getenv("MAIL_USERNAME"),
                password=os.getenv("MAIL_PASSWORD"),
                use_tls=os.getenv("MAIL_TLS_ENCRYPTION", "True") == "True",
                use_ssl=os.getenv("MAIL_SSL_ENCRYPTION", "False") == "True",
            )
        elif provider_name == "sendgrid":
            return SendGridProvider(
                api_key=os.getenv("MAIL_API_KEY"),
                endpoint=os.getenv("MAIL_ENDPOINT"),
            )
        elif provider_name == "mailgun":
            return MailgunProvider(
                api_key=os.getenv("MAIL_API_KEY"),
                endpoint=os.getenv("MAIL_ENDPOINT"),
            )
        elif provider_name == "ses":
            return SESProvider(
                aws_access_key_id=os.getenv("MAIL_AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("MAIL_AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("MAIL_AWS_REGION"),
            )
        elif provider_name == "postmark":
            return PostmarkProvider(
                server_token=os.getenv("MAIL_API_KEY"),
                endpoint=os.getenv("MAIL_ENDPOINT"),
            )
        elif provider_name == "brevo":
            return BrevoProvider(
                api_key=os.getenv("MAIL_API_KEY"),
                endpoint=os.getenv("MAIL_ENDPOINT"),
            )
        else:
            raise ValueError(f"Unsupported mail provider: {provider_name}")