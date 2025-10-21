import smtplib
from email.mime.text import MIMEText
from .provider_interface import ProviderInterface

class SMTPProvider(ProviderInterface):
    def __init__(self, host: str, port: int, username: str, password: str, use_tls: bool = True, use_ssl: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl

    def send(self, to: str, subject: str, body: str, from_email: str = None) -> bool:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = from_email or self.username
        msg["To"] = to

        try:
            if self.use_ssl:
                # SMTP over SSL (port 465)
                with smtplib.SMTP_SSL(self.host, self.port) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                # SMTP with STARTTLS (port 587)
                with smtplib.SMTP(self.host, self.port) as server:
                    server.ehlo()  # Initialize connection
                    if self.use_tls:
                        server.starttls()
                        server.ehlo()
                    if self.username and self.password:
                        server.login(self.username, self.password)
                    server.send_message(msg)
            return True
        except smtplib.SMTPException as e:
            print(f"[MailBridge] Error sending email: {e}")
            return False
