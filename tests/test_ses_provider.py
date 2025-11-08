"""
Unit tests for SES (Amazon Simple Email Service) provider.

Tests cover:
- Configuration validation
- Regular email sending
- Template email sending
- Bulk email sending (with 50 limit)
- Raw email with attachments
- Error handling

Run with: pytest tests/test_ses_provider.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from mailbridge.providers.ses_provider import SESProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO
from mailbridge.exceptions import ConfigurationError, EmailSendError


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def ses_config():
    """SES configuration fixture."""
    return {
        'aws_access_key_id': 'AKIAXXXXXXXXXXXXXXXX',
        'aws_secret_access_key': 'secretkey123456789',
        'region_name': 'us-east-1',
        'from_email': 'sender@example.com'
    }


@pytest.fixture
def ses_provider(ses_config):
    """SES provider fixture."""
    with patch('mailbridge.providers.ses_provider.boto3.client'):
        return SESProvider(**ses_config)


@pytest.fixture
def simple_message():
    """Simple email message fixture."""
    return EmailMessageDto(
        to='recipient@example.com',
        subject='Test Email',
        body='<h1>Hello World</h1>',
        html=True
    )


@pytest.fixture
def template_message():
    """Template email message fixture."""
    return EmailMessageDto(
        to='recipient@example.com',
        template_id='WelcomeTemplate',
        template_data={
            'name': 'John Doe',
            'company': 'Acme Corp'
        }
    )


@pytest.fixture
def mock_ses_client():
    """Mock boto3 SES client."""
    mock_client = Mock()
    mock_client.send_email.return_value = {
        'MessageId': 'ses-message-id-123',
        'ResponseMetadata': {'RequestId': 'request-id-456'}
    }
    mock_client.send_templated_email.return_value = {
        'MessageId': 'ses-template-id-789',
        'ResponseMetadata': {'RequestId': 'request-id-abc'}
    }
    mock_client.send_bulk_templated_email.return_value = {
        'Status': [
            {'Status': 'Success', 'MessageId': 'msg1'},
            {'Status': 'Success', 'MessageId': 'msg2'},
            {'Status': 'Success', 'MessageId': 'msg3'}
        ],
        'ResponseMetadata': {'RequestId': 'bulk-request-id'}
    }
    return mock_client


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

class TestSESConfiguration:
    """Test SES provider configuration."""

    @patch('mailbridge.providers.ses_provider.boto3.client')
    def test_valid_configuration(self, mock_boto_client, ses_config):
        """Test provider initializes with valid config."""
        provider = SESProvider(**ses_config)

        assert provider.aws_access_key_id == 'AKIAXXXXXXXXXXXXXXXX'
        assert provider.region_name == 'us-east-1'

        # Check boto3.client was called correctly
        mock_boto_client.assert_called_once_with(
            'ses',
            region_name='us-east-1',
            aws_access_key_id='AKIAXXXXXXXXXXXXXXXX',
            aws_secret_access_key='secretkey123456789'
        )

    @patch('mailbridge.providers.ses_provider.boto3.client')
    def test_iam_role_configuration(self, mock_boto_client):
        """Test provider works with IAM role (no explicit keys)."""
        config = {
            'region_name': 'us-west-2',
            'from_email': 'sender@example.com'
        }

        provider = SESProvider(**config)

        # Should not include credentials
        mock_boto_client.assert_called_once_with(
            'ses',
            region_name='us-west-2'
        )

    @patch('mailbridge.providers.ses_provider.BOTO3_AVAILABLE', False)
    def test_missing_boto3(self):
        """Test provider raises error when boto3 is not installed."""
        with pytest.raises(ConfigurationError) as exc_info:
            SESProvider(region_name='us-east-1')

        assert 'boto3 is required' in str(exc_info.value)

    @patch('mailbridge.providers.ses_provider.boto3.client')
    def test_default_region(self, mock_boto_client):
        """Test provider uses default region."""
        config = {'from_email': 'sender@example.com'}
        provider = SESProvider(**config)

        assert provider.region_name == 'us-east-1'

    def test_supports_templates(self, ses_provider):
        """Test provider indicates template support."""
        assert ses_provider.supports_templates() is True

    def test_supports_bulk_sending(self, ses_provider):
        """Test provider indicates bulk sending support."""
        assert ses_provider.supports_bulk_sending() is True


# =============================================================================
# REGULAR EMAIL TESTS
# =============================================================================

class TestSESRegularEmail:
    """Test regular email sending."""

    def test_send_simple_email(self, ses_provider, simple_message, mock_ses_client):
        """Test sending a simple email via send_email."""
        ses_provider.client = mock_ses_client

        response = ses_provider.send(simple_message)

        # Check response
        assert response.success is True
        assert response.message_id == 'ses-message-id-123'
        assert response.provider == 'ses'
        assert 'request_id' in response.metadata

        # Check SES API call
        mock_ses_client.send_email.assert_called_once()
        call_kwargs = mock_ses_client.send_email.call_args[1]

        assert call_kwargs['Source'] == 'sender@example.com'
        assert call_kwargs['Destination']['ToAddresses'] == ['recipient@example.com']
        assert call_kwargs['Message']['Subject']['Data'] == 'Test Email'
        assert call_kwargs['Message']['Body']['Html']['Data'] == '<h1>Hello World</h1>'

    def test_send_plain_text(self, ses_provider, mock_ses_client):
        """Test sending plain text email."""
        ses_provider.client = mock_ses_client

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Plain Text',
            body='Plain text content',
            html=False
        )

        response = ses_provider.send(message)

        assert response.success is True

        call_kwargs = mock_ses_client.send_email.call_args[1]
        assert 'Text' in call_kwargs['Message']['Body']
        assert call_kwargs['Message']['Body']['Text']['Data'] == 'Plain text content'

    def test_send_with_cc_bcc(self, ses_provider, mock_ses_client):
        """Test sending email with CC and BCC."""
        ses_provider.client = mock_ses_client

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Test',
            body='Body',
            cc=['cc@example.com'],
            bcc=['bcc@example.com']
        )

        response = ses_provider.send(message)

        assert response.success is True

        call_kwargs = mock_ses_client.send_email.call_args[1]
        assert call_kwargs['Destination']['CcAddresses'] == ['cc@example.com']
        assert call_kwargs['Destination']['BccAddresses'] == ['bcc@example.com']

    def test_send_with_reply_to(self, ses_provider, mock_ses_client):
        """Test sending email with Reply-To."""
        ses_provider.client = mock_ses_client

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Test',
            body='Body',
            reply_to='reply@example.com'
        )

        response = ses_provider.send(message)

        assert response.success is True

        call_kwargs = mock_ses_client.send_email.call_args[1]
        assert call_kwargs['ReplyToAddresses'] == ['reply@example.com']

    def test_send_with_attachments_uses_raw(self, ses_provider, mock_ses_client, tmp_path):
        """Test that email with attachments uses send_raw_email."""
        ses_provider.client = mock_ses_client
        mock_ses_client.send_raw_email.return_value = {
            'MessageId': 'raw-message-id',
            'ResponseMetadata': {'RequestId': 'raw-request-id'}
        }

        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='With Attachment',
            body='Body',
            attachments=[test_file]
        )

        response = ses_provider.send(message)

        assert response.success is True
        assert response.message_id == 'raw-message-id'

        # Should call send_raw_email, not send_email
        mock_ses_client.send_raw_email.assert_called_once()
        mock_ses_client.send_email.assert_not_called()

    def test_send_client_error(self, ses_provider, simple_message):
        """Test handling of SES ClientError."""
        from botocore.exceptions import ClientError

        ses_provider.client = Mock()
        ses_provider.client.send_email.side_effect = ClientError(
            {'Error': {'Code': 'MessageRejected', 'Message': 'Email not verified'}},
            'send_email'
        )

        with pytest.raises(EmailSendError) as exc_info:
            ses_provider.send(simple_message)

        assert 'SES error (MessageRejected)' in str(exc_info.value)
        assert 'Email not verified' in str(exc_info.value)


# =============================================================================
# TEMPLATE EMAIL TESTS
# =============================================================================

class TestSESTemplateEmail:
    """Test template email sending."""

    def test_send_template_email(self, ses_provider, template_message, mock_ses_client):
        """Test sending a template email."""
        ses_provider.client = mock_ses_client

        response = ses_provider.send(template_message)

        assert response.success is True
        assert response.message_id == 'ses-template-id-789'
        assert response.metadata['template_id'] == 'WelcomeTemplate'

        # Check API call
        mock_ses_client.send_templated_email.assert_called_once()
        call_kwargs = mock_ses_client.send_templated_email.call_args[1]

        assert call_kwargs['Template'] == 'WelcomeTemplate'
        assert call_kwargs['Destination']['ToAddresses'] == ['recipient@example.com']

        # Check template data is JSON string
        template_data = json.loads(call_kwargs['TemplateData'])
        assert template_data['name'] == 'John Doe'
        assert template_data['company'] == 'Acme Corp'

    def test_template_data_serialization(self, ses_provider):
        """Test that template data is properly serialized to JSON."""
        data = {'name': 'Test', 'count': 123, 'active': True}

        serialized = ses_provider._serialize_template_data(data)

        assert isinstance(serialized, str)
        parsed = json.loads(serialized)
        assert parsed == data

    def test_template_with_empty_data(self, ses_provider, mock_ses_client):
        """Test template email with no template data."""
        ses_provider.client = mock_ses_client

        message = EmailMessageDto(
            to='recipient@example.com',
            template_id='SimpleTemplate',
            template_data=None
        )

        response = ses_provider.send(message)

        assert response.success is True

        call_kwargs = mock_ses_client.send_templated_email.call_args[1]
        assert call_kwargs['TemplateData'] == '{}'


# =============================================================================
# BULK EMAIL TESTS
# =============================================================================

class TestSESBulkEmail:
    """Test bulk email sending."""

    def test_send_bulk_template_emails(self, ses_provider, mock_ses_client):
        """Test sending bulk template emails."""
        ses_provider.client = mock_ses_client

        messages = [
            EmailMessageDto(
                to='user1@example.com',
                template_id='Newsletter',
                template_data={'name': 'Alice'}
            ),
            EmailMessageDto(
                to='user2@example.com',
                template_id='Newsletter',
                template_data={'name': 'Bob'}
            ),
            EmailMessageDto(
                to='user3@example.com',
                template_id='Newsletter',
                template_data={'name': 'Charlie'}
            ),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = ses_provider.send_bulk(bulk)

        assert result.total == 1  # One batch
        assert result.successful == 1
        assert result.failed == 0

        # Check API call
        mock_ses_client.send_bulk_templated_email.assert_called_once()
        call_kwargs = mock_ses_client.send_bulk_templated_email.call_args[1]

        assert call_kwargs['Template'] == 'Newsletter'
        assert len(call_kwargs['Destinations']) == 3

        # Check personalizations
        dest1 = call_kwargs['Destinations'][0]
        assert dest1['Destination']['ToAddresses'] == ['user1@example.com']
        template_data1 = json.loads(dest1['ReplacementTemplateData'])
        assert template_data1['name'] == 'Alice'

    def test_bulk_respects_50_limit(self, ses_provider, mock_ses_client):
        """Test that bulk sending respects SES 50 destination limit."""
        ses_provider.client = mock_ses_client

        # Create 75 messages
        messages = [
            EmailMessageDto(
                to=f'user{i}@example.com',
                template_id='Template',
                template_data={'name': f'User{i}'}
            )
            for i in range(75)
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = ses_provider.send_bulk(bulk)

        # Should be split into 2 batches (50 + 25)
        assert mock_ses_client.send_bulk_templated_email.call_count == 2

        # Check first batch has 50
        first_call = mock_ses_client.send_bulk_templated_email.call_args_list[0]
        assert len(first_call[1]['Destinations']) == 50

        # Check second batch has 25
        second_call = mock_ses_client.send_bulk_templated_email.call_args_list[1]
        assert len(second_call[1]['Destinations']) == 25

    def test_send_bulk_regular_emails(self, ses_provider, mock_ses_client):
        """Test bulk sending of regular emails (no bulk API)."""
        ses_provider.client = mock_ses_client

        messages = [
            EmailMessageDto(to='user1@example.com', subject='Test 1', body='Body 1'),
            EmailMessageDto(to='user2@example.com', subject='Test 2', body='Body 2'),
            EmailMessageDto(to='user3@example.com', subject='Test 3', body='Body 3'),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = ses_provider.send_bulk(bulk)

        assert result.total == 3
        assert result.successful == 3

        # Should call send_email for each
        assert mock_ses_client.send_email.call_count == 3

    def test_send_bulk_mixed(self, ses_provider, mock_ses_client):
        """Test bulk with mix of template and regular emails."""
        ses_provider.client = mock_ses_client

        messages = [
            # Template emails
            EmailMessageDto(to='user1@example.com', template_id='Welcome', template_data={'name': 'Alice'}),
            EmailMessageDto(to='user2@example.com', template_id='Welcome', template_data={'name': 'Bob'}),
            # Regular email
            EmailMessageDto(to='admin@example.com', subject='Report', body='Admin report'),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = ses_provider.send_bulk(bulk)

        # 1 template batch + 1 regular email = 2 responses
        assert result.total == 2

        # Check both APIs were called
        mock_ses_client.send_bulk_templated_email.assert_called_once()
        mock_ses_client.send_email.assert_called_once()

    def test_bulk_multiple_templates(self, ses_provider, mock_ses_client):
        """Test bulk with different template IDs."""
        ses_provider.client = mock_ses_client

        messages = [
            EmailMessageDto(to='user1@example.com', template_id='Welcome', template_data={'name': 'Alice'}),
            EmailMessageDto(to='user2@example.com', template_id='Welcome', template_data={'name': 'Bob'}),
            EmailMessageDto(to='user3@example.com', template_id='Newsletter', template_data={'month': 'Nov'}),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = ses_provider.send_bulk(bulk)

        # Should be grouped by template_id: 2 batches
        assert mock_ses_client.send_bulk_templated_email.call_count == 2


# =============================================================================
# RAW EMAIL TESTS
# =============================================================================

class TestSESRawEmail:
    """Test raw email sending (with attachments)."""

    def test_send_raw_email_with_attachment(self, ses_provider, mock_ses_client, tmp_path):
        """Test sending raw email with attachment."""
        ses_provider.client = mock_ses_client
        mock_ses_client.send_raw_email.return_value = {
            'MessageId': 'raw-id-123',
            'ResponseMetadata': {'RequestId': 'raw-request-123'}
        }

        test_file = tmp_path / "document.pdf"
        test_file.write_bytes(b'PDF content')

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='With PDF',
            body='Please see attached PDF',
            attachments=[test_file]
        )

        response = ses_provider.send(message)

        assert response.success is True
        assert response.message_id == 'raw-id-123'

        # Check send_raw_email was called
        mock_ses_client.send_raw_email.assert_called_once()
        call_kwargs = mock_ses_client.send_raw_email.call_args[1]

        assert call_kwargs['Source'] == 'sender@example.com'
        assert call_kwargs['Destinations'] == ['recipient@example.com']
        assert 'RawMessage' in call_kwargs

    def test_raw_email_with_tuple_attachment(self, ses_provider, mock_ses_client):
        """Test raw email with tuple attachment."""
        ses_provider.client = mock_ses_client
        mock_ses_client.send_raw_email.return_value = {
            'MessageId': 'raw-id-456',
            'ResponseMetadata': {'RequestId': 'raw-request-456'}
        }

        attachment = ('report.csv', b'col1,col2\nval1,val2', 'text/csv')

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='CSV Report',
            body='Report attached',
            attachments=[attachment]
        )

        response = ses_provider.send(message)

        assert response.success is True
        mock_ses_client.send_raw_email.assert_called_once()


# =============================================================================
# HELPER METHODS TESTS
# =============================================================================

class TestSESHelpers:
    """Test helper methods."""

    def test_serialize_template_data(self, ses_provider):
        """Test template data serialization."""
        data = {
            'name': 'John',
            'age': 30,
            'active': True,
            'items': ['a', 'b', 'c']
        }

        result = ses_provider._serialize_template_data(data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data


# =============================================================================
# CONTEXT MANAGER TESTS
# =============================================================================

class TestSESContextManager:
    """Test context manager support."""

    @patch('mailbridge.providers.ses_provider.boto3.client')
    def test_context_manager(self, mock_boto_client, ses_config):
        """Test using provider as context manager."""
        with SESProvider(**ses_config) as provider:
            assert provider is not None
            assert isinstance(provider, SESProvider)


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])