import smtplib
from email.mime.text import MIMEText
from .provider_interface import ProviderInterface

class SMTPProvider(ProviderInterface):
    def __init__(self, host, port, username, password, use_tls=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send(self, to:str, subject: str, body: str, from_email: str = None):
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = from_email or self.username
        msg["To"] = to

        with smtplib.SMTP(self.host, self.port) as server:
            if self.use_tls:
                server.starttls()
            if self.username and self.password:
                server.login(self.username, self.password)
            server.send_message(msg)
        return True