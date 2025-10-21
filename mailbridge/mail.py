from .mailer_factory import MailerFactory

class Mail:
    @staticmethod
    def send(to: str, subject: str, body: str, from_email: str = None) -> bool:
        """
        Sends an email using the configured provider from environment variables.

        :param to: Recipient email
        :param subject: Email subject
        :param body: HTML body of the email
        :param from_email: Optional sender email; if None, provider default is used
        :return: True if email was sent successfully, False otherwise
        """
        try:
            provider = MailerFactory.get_provider()
            return provider.send(to=to, subject=subject, body=body, from_email=from_email)
        except Exception as e:
            # Optional: log error (e.g., with logging library)
            print(f"[MailBridge] Error sending email: {e}")
            return False
