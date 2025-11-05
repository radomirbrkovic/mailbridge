from pathlib import Path
from typing import Dict, Any, List, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from mailbridge.providers.base_email_provider import BaseEmailProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.exceptions import ConfigurationError, EmailSendError

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

class SESProvider(BaseEmailProvider):

    def send(self, message: EmailMessageDto) -> Dict[str, Any]:
        pass

    def _validate_config(self) -> None:
        """Validate SES configuration."""
        if not BOTO3_AVAILABLE:
            raise ConfigurationError(
                "boto3 is required for SES provider. "
                "Install it with: pip install mailbridge[ses]"
            )

        self.aws_access_key_id = self.config.get('aws_access_key_id')
        self.aws_secret_access_key = self.config.get('aws_secret_access_key')
        self.region_name = self.config.get('region_name', 'us-east-1')

        try:
            session_params = {
                'region_name': self.region_name
            }
            if self.aws_access_key_id and self.aws_secret_access_key:
                session_params['aws_access_key_id'] = self.aws_access_key_id
                session_params['aws_secret_access_key'] = self.aws_secret_access_key

            self.client = boto3.client('ses', **session_params)
        except Exception as e:
            raise ConfigurationError(f"Failed to create SES client: {str(e)}")

    def _send_simple_email(self, message: EmailMessageDto) -> Dict[str, Any]:
        destination = {
            'ToAddresses': message.to
        }

        if message.cc:
            destination['CcAddresses'] = message.cc
        if message.bcc:
            destination['BccAddresses'] = message.bcc

        email_message = {
            'Subject': {
                'Data': message.subject,
                'Charset': 'UTF-8'
            },
            'Body': {}
        }

        if message.html:
            email_message['Body']['Html'] = {
                'Data': message.body,
                'Charset': 'UTF-8'
            }
        else:
            email_message['Body']['Text'] = {
                'Data': message.body,
                'Charset': 'UTF-8'
            }

        params = {
            'Source': message.from_email or self.config.get('from_email'),
            'Destination': destination,
            'Message': email_message
        }

        if message.reply_to:
            params['ReplyToAddresses'] = [message.reply_to]

        response = self.client.send_email(**params)

        return {
            'success': True,
            'message_id': response['MessageId'],
            'provider': 'ses'
        }