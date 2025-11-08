"""
Unit tests for Postmark provider.

Tests cover:
- Configuration validation
- Regular email sending
- Template email sending
- Bulk email sending
- Attachments
- Tracking options
- Error handling

Run with: pytest tests/test_postmark_provider.py -v
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import base64

from mailbridge.providers.postmark_provider import PostmarkProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.dto.email_response_dto import EmailResponseDTO
from mailbridge.dto.bulk_email_response_dto import BulkEmailResponseDTO
from mailbridge.exceptions import ConfigurationError, EmailSendError


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def postmark_config():
    """Postmark configuration fixture."""
    return {
        'server_token': 'test-server-token-12345',
        'from_email': 'sender@example.com'
    }


@pytest.fixture
def postmark_provider(postmark_config):
    """Postmark provider fixture."""
    return PostmarkProvider(**postmark_config)


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
        template_id='welcome-template',
        template_data={
            'product_name': 'Pro Plan',
            'name': 'John',
            'action_url': 'https://example.com/activate'
        }
    )


@pytest.fixture
def mock_postmark_response():
    """Mock Postmark API response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'MessageID': 'postmark-message-id-123',
        'SubmittedAt': '2024-01-15T10:30:00Z',
        'To': 'recipient@example.com'
    }
    return mock_response


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

class TestPostmarkConfiguration:
    """Test Postmark provider configuration."""

    def test_valid_configuration(self, postmark_config):
        """Test provider initializes with valid config."""
        provider = PostmarkProvider(**postmark_config)

        assert provider.config['server_token'] == 'test-server-token-12345'
        assert provider.config['from_email'] == 'sender@example.com'
        assert provider.endpoint == 'https://api.postmarkapp.com/email'

    def test_custom_endpoint(self, postmark_config):
        """Test provider accepts custom endpoint."""
        postmark_config['endpoint'] = 'https://custom.postmarkapp.com/email'
        provider = PostmarkProvider(**postmark_config)

        assert provider.endpoint == 'https://custom.postmarkapp.com/email'

    def test_missing_server_token(self):
        """Test provider raises error when server_token is missing."""
        with pytest.raises(ConfigurationError) as exc_info:
            PostmarkProvider(from_email='sender@example.com')

        assert 'server_token' in str(exc_info.value)

    def test_supports_templates(self, postmark_provider):
        """Test provider indicates template support."""
        assert postmark_provider.supports_templates() is True

    def test_supports_bulk_sending(self, postmark_provider):
        """Test provider indicates bulk sending support."""
        assert postmark_provider.supports_bulk_sending() is True


# =============================================================================
# REGULAR EMAIL TESTS
# =============================================================================

class TestPostmarkRegularEmail:
    """Test regular email sending."""

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_simple_email(self, mock_post, postmark_provider, simple_message, mock_postmark_response):
        """Test sending a simple email."""
        mock_post.return_value = mock_postmark_response

        response = postmark_provider.send(simple_message)

        # Check response
        assert response.success is True
        assert response.message_id == 'postmark-message-id-123'
        assert response.provider == 'postmark'
        assert response.metadata['submitted_at'] == '2024-01-15T10:30:00Z'
        assert response.metadata['to'] == 'recipient@example.com'

        # Check API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Check endpoint
        assert call_args[0][0] == 'https://api.postmarkapp.com/email'

        # Check headers
        headers = call_args[1]['headers']
        assert headers['X-Postmark-Server-Token'] == 'test-server-token-12345'
        assert headers['Content-Type'] == 'application/json'

        # Check payload
        payload = call_args[1]['json']
        assert payload['From'] == 'sender@example.com'
        assert payload['To'] == 'recipient@example.com'
        assert payload['Subject'] == 'Test Email'
        assert payload['HtmlBody'] == '<h1>Hello World</h1>'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_plain_text(self, mock_post, postmark_provider, mock_postmark_response):
        """Test sending plain text email."""
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Plain Text',
            body='Plain text content',
            html=False
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert 'TextBody' in payload
        assert payload['TextBody'] == 'Plain text content'
        assert 'HtmlBody' not in payload

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_cc_bcc(self, mock_post, postmark_provider, mock_postmark_response):
        """Test sending email with CC and BCC."""
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Test',
            body='Body',
            cc=['cc@example.com'],
            bcc=['bcc@example.com']
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['Cc'] == 'cc@example.com'
        assert payload['Bcc'] == 'bcc@example.com'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_reply_to(self, mock_post, postmark_provider, mock_postmark_response):
        """Test sending email with Reply-To."""
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Test',
            body='Body',
            reply_to='reply@example.com'
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['ReplyTo'] == 'reply@example.com'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_custom_headers(self, mock_post, postmark_provider, mock_postmark_response):
        """Test sending email with custom headers."""
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Test',
            body='Body',
            headers={'X-Custom-Header': 'custom-value', 'X-Priority': '1'}
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert 'Headers' in payload
        assert len(payload['Headers']) == 2
        assert {'Name': 'X-Custom-Header', 'Value': 'custom-value'} in payload['Headers']
        assert {'Name': 'X-Priority', 'Value': '1'} in payload['Headers']

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_attachments(self, mock_post, postmark_provider, mock_postmark_response, tmp_path):
        """Test sending email with attachments."""
        mock_post.return_value = mock_postmark_response

        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='With Attachment',
            body='See attached file',
            attachments=[test_file]
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert 'Attachments' in payload
        assert len(payload['Attachments']) == 1
        assert payload['Attachments'][0]['Name'] == 'test.txt'
        assert payload['Attachments'][0]['ContentType'] == 'application/octet-stream'

        # Check base64 encoding
        content = base64.b64decode(payload['Attachments'][0]['Content'])
        assert content.decode() == 'Test content'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_tuple_attachment(self, mock_post, postmark_provider, mock_postmark_response):
        """Test sending email with tuple attachment."""
        mock_post.return_value = mock_postmark_response

        attachment = ('report.pdf', b'PDF content', 'application/pdf')

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='PDF Report',
            body='Report attached',
            attachments=[attachment]
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['Attachments'][0]['Name'] == 'report.pdf'
        assert payload['Attachments'][0]['ContentType'] == 'application/pdf'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_with_tracking_options(self, mock_post, mock_postmark_response):
        """Test sending with tracking options."""
        config = {
            'server_token': 'test-token',
            'track_opens': True,
            'track_links': 'HtmlAndText'
        }
        provider = PostmarkProvider(**config)
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Tracked Email',
            body='Track me'
        )

        response = provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['TrackOpens'] is True
        assert payload['TrackLinks'] == 'HtmlAndText'

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_api_error(self, mock_post, postmark_provider, simple_message):
        """Test handling of Postmark API error."""
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            'ErrorCode': 300,
            'Message': 'Invalid email request'
        }
        mock_post.return_value = mock_response

        with pytest.raises(EmailSendError) as exc_info:
            postmark_provider.send(simple_message)

        assert 'Postmark API error' in str(exc_info.value)
        assert '300' in str(exc_info.value)

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_network_error(self, mock_post, postmark_provider, simple_message):
        """Test handling of network error."""
        import requests
        mock_post.side_effect = requests.ConnectionError('Network error')

        with pytest.raises(EmailSendError) as exc_info:
            postmark_provider.send(simple_message)

        assert 'Failed to send email via Postmark' in str(exc_info.value)


# =============================================================================
# TEMPLATE EMAIL TESTS
# =============================================================================

class TestPostmarkTemplateEmail:
    """Test template email sending."""

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_template_email(self, mock_post, postmark_provider, template_message, mock_postmark_response):
        """Test sending a template email."""
        mock_post.return_value = mock_postmark_response

        response = postmark_provider.send(template_message)

        assert response.success is True
        assert response.message_id == 'postmark-message-id-123'

        # Check payload
        payload = mock_post.call_args[1]['json']
        assert payload['TemplateId'] == 'welcome-template'
        assert payload['TemplateModel'] == {
            'product_name': 'Pro Plan',
            'name': 'John',
            'action_url': 'https://example.com/activate'
        }

        # Should NOT have HtmlBody or TextBody
        assert 'HtmlBody' not in payload
        assert 'TextBody' not in payload

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_template_with_empty_data(self, mock_post, postmark_provider, mock_postmark_response):
        """Test template email with no template data."""
        mock_post.return_value = mock_postmark_response

        message = EmailMessageDto(
            to='recipient@example.com',
            template_id='simple-template',
            template_data=None
        )

        response = postmark_provider.send(message)

        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['TemplateModel'] is None

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_template_detection(self, mock_post, postmark_provider, template_message):
        """Test that template emails are properly detected."""
        mock_post.return_value = Mock(
            status_code=200,
            json=Mock(return_value={'MessageID': 'test', 'SubmittedAt': '', 'To': ''})
        )

        assert template_message.is_template_email() is True

        postmark_provider.send(template_message)

        payload = mock_post.call_args[1]['json']
        assert 'TemplateId' in payload


# =============================================================================
# BULK EMAIL TESTS
# =============================================================================

class TestPostmarkBulkEmail:
    """Test bulk email sending."""

    @patch('mailbridge.providers.postmark_provider.requests.post')
    def test_send_bulk_emails(self, mock_post, postmark_provider):
        """Test sending bulk emails (loops through each)."""
        mock_response = Mock(
            status_code=200,
            json=Mock(return_value={'MessageID': 'bulk-id', 'SubmittedAt': '', 'To': ''})
        )
        mock_post.return_value = mock_response

        messages = [
            EmailMessageDto(to='user1@example.com', subject='Test 1', body='Body 1'),
            EmailMessageDto(to='user2@example.com', subject='Test 2', body='Body 2'),
            EmailMessageDto(to='user3@example.com', subject='Test 3', body='Body 3'),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = postmark_provider.send_bulk(bulk)

        assert result.total == 3
        assert result.successful == 3
        assert result.failed == 0

        # Should call send() for each message (no native bulk API used)
        assert mock_post.call_count == 3


# =============================================================================
# HELPER METHODS TESTS
# =============================================================================

class TestPostmarkHelpers:
    """Test helper methods."""

    def test_build_payload_regular(self, postmark_provider):
        """Test _build_payload for regular email."""
        message = EmailMessageDto(
            to='test@example.com',
            subject='Test Subject',
            body='<p>Test body</p>',
            html=True
        )

        payload = postmark_provider._build_payload(message)

        assert payload['From'] == 'sender@example.com'
        assert payload['To'] == 'test@example.com'
        assert payload['Subject'] == 'Test Subject'
        assert payload['HtmlBody'] == '<p>Test body</p>'

    def test_build_payload_template(self, postmark_provider):
        """Test _build_payload for template email."""
        message = EmailMessageDto(
            to='test@example.com',
            template_id='my-template',
            template_data={'key': 'value'}
        )

        payload = postmark_provider._build_payload(message)

        assert payload['TemplateId'] == 'my-template'
        assert payload['TemplateModel'] == {'key': 'value'}
        assert 'HtmlBody' not in payload
        assert 'TextBody' not in payload

    def test_build_attachments(self, postmark_provider, tmp_path):
        """Test _build_attachments helper."""
        test_file = tmp_path / "document.txt"
        test_file.write_text("Content")

        tuple_attachment = ('file.csv', b'csv,data', 'text/csv')

        attachments = [test_file, tuple_attachment]

        result = postmark_provider._build_attachments(attachments)

        assert len(result) == 2

        # Check file attachment
        assert result[0]['Name'] == 'document.txt'
        assert result[0]['ContentType'] == 'application/octet-stream'

        # Check tuple attachment
        assert result[1]['Name'] == 'file.csv'
        assert result[1]['ContentType'] == 'text/csv'


# =============================================================================
# CONTEXT MANAGER TESTS
# =============================================================================

class TestPostmarkContextManager:
    """Test context manager support."""

    def test_context_manager(self, postmark_config):
        """Test using provider as context manager."""
        with PostmarkProvider(**postmark_config) as provider:
            assert provider is not None
            assert isinstance(provider, PostmarkProvider)


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])