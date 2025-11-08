"""
Unit tests for Brevo provider.

Tests cover:
- Configuration validation
- Regular email sending
- Template email sending
- Bulk email sending
- Error handling
- Attachments
- CC/BCC/Reply-To

Run with: pytest tests/test_brevo_provider.py -v
"""

import pytest
from unittest.mock import Mock, patch
import base64

from mailbridge.providers.brevo_provider import BrevoProvider
from mailbridge.dto.email_message_dto import EmailMessageDto
from mailbridge.dto.bulk_email_dto import BulkEmailDTO
from mailbridge.exceptions import ConfigurationError, EmailSendError


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def brevo_config():
    """Brevo configuration fixture."""
    return {
        'api_key': 'xkeysib-123456789abcdef',
        'from_email': 'sender@example.com'
    }


@pytest.fixture
def brevo_provider(brevo_config):
    """Brevo provider fixture."""
    return BrevoProvider(**brevo_config)


@pytest.fixture
def simple_message():
    """Simple email message fixture."""
    return EmailMessageDto(
        to='recipient@example.com',
        subject='Test Email',
        body='<h1>Hello Brevo</h1>',
        html=True
    )


@pytest.fixture
def template_message():
    """Template email message fixture."""
    return EmailMessageDto(
        to='recipient@example.com',
        template_id=12,
        template_data={
            'name': 'John Doe',
            'company': 'Acme Corp'
        }
    )


@pytest.fixture
def mock_response_success():
    """Mock successful Brevo response."""
    mock_resp = Mock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {'messageId': 'brevo_message_123'}
    return mock_resp


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

class TestBrevoConfiguration:
    """Test Brevo provider configuration."""

    def test_valid_configuration(self, brevo_config):
        provider = BrevoProvider(**brevo_config)
        assert provider.config['api_key'] == 'xkeysib-123456789abcdef'
        assert provider.endpoint == 'https://api.brevo.com/v3/smtp/email'

    def test_custom_endpoint(self, brevo_config):
        brevo_config['endpoint'] = 'https://custom.brevo.test'
        provider = BrevoProvider(**brevo_config)
        assert provider.endpoint == 'https://custom.brevo.test'

    def test_missing_api_key(self):
        with pytest.raises(ConfigurationError) as exc:
            BrevoProvider(from_email='sender@example.com')
        assert 'api_key' in str(exc.value)


# =============================================================================
# REGULAR EMAIL TESTS
# =============================================================================

class TestBrevoRegularEmail:
    """Test sending of regular Brevo emails."""

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_simple_email(self, mock_post, brevo_provider, simple_message, mock_response_success):
        mock_post.return_value = mock_response_success

        response = brevo_provider.send(simple_message)
        assert response.success is True
        assert response.message_id == 'brevo_message_123'
        assert response.provider == 'brevo'

        call_args = mock_post.call_args
        assert call_args[0][0] == 'https://api.brevo.com/v3/smtp/email'

        headers = call_args[1]['headers']
        assert headers['api-key'] == 'xkeysib-123456789abcdef'
        assert headers['Content-Type'] == 'application/json'

        payload = call_args[1]['json']
        assert payload['sender']['email'] == 'sender@example.com'
        assert payload['to'][0]['email'] == 'recipient@example.com'
        assert payload['subject'] == 'Test Email'
        assert payload['htmlContent'] == '<h1>Hello Brevo</h1>'

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_with_cc_bcc_replyto(self, mock_post, brevo_provider, mock_response_success):
        mock_post.return_value = mock_response_success

        message = EmailMessageDto(
            to='to@example.com',
            subject='Test CC BCC',
            body='Body',
            cc=['cc1@example.com'],
            bcc=['bcc1@example.com'],
            reply_to='reply@example.com'
        )

        response = brevo_provider.send(message)
        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['cc'][0]['email'] == 'cc1@example.com'
        assert payload['bcc'][0]['email'] == 'bcc1@example.com'
        assert payload['replyTo']['email'] == 'reply@example.com'

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_with_headers(self, mock_post, brevo_provider, mock_response_success):
        mock_post.return_value = mock_response_success

        message = EmailMessageDto(
            to='to@example.com',
            subject='Header Test',
            body='Header body',
            headers={'X-Custom': 'Yes'}
        )
        brevo_provider.send(message)

        payload = mock_post.call_args[1]['json']
        assert payload['headers']['X-Custom'] == 'Yes'

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_plain_text(self, mock_post, brevo_provider, mock_response_success):
        mock_post.return_value = mock_response_success

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Plain Test',
            body='Plain body',
            html=False
        )

        brevo_provider.send(message)
        payload = mock_post.call_args[1]['json']
        assert payload['textContent'] == 'Plain body'
        assert 'htmlContent' not in payload

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_with_attachment_file(self, mock_post, brevo_provider, mock_response_success, tmp_path):
        mock_post.return_value = mock_response_success

        test_file = tmp_path / "test.txt"
        test_file.write_text("File content")

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Attachment Test',
            body='See file',
            attachments=[test_file]
        )

        brevo_provider.send(message)
        payload = mock_post.call_args[1]['json']
        assert len(payload['attachment']) == 1
        assert payload['attachment'][0]['name'] == 'test.txt'
        decoded = base64.b64decode(payload['attachment'][0]['content']).decode()
        assert decoded == 'File content'

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_with_tuple_attachment(self, mock_post, brevo_provider, mock_response_success):
        mock_post.return_value = mock_response_success

        attachment = ('file.pdf', b'data123', 'application/pdf')
        message = EmailMessageDto(
            to='recipient@example.com',
            subject='Attachment Tuple',
            body='See attached',
            attachments=[attachment]
        )

        brevo_provider.send(message)
        payload = mock_post.call_args[1]['json']
        assert payload['attachment'][0]['name'] == 'file.pdf'
        decoded = base64.b64decode(payload['attachment'][0]['content']).decode()
        assert decoded == 'data123'

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_api_error(self, mock_post, brevo_provider, simple_message):
        mock_resp = Mock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {'code': 'invalid_email', 'message': 'Invalid email address'}
        mock_post.return_value = mock_resp

        with pytest.raises(EmailSendError) as exc:
            brevo_provider.send(simple_message)
        assert 'Brevo API error' in str(exc.value)
        assert 'invalid_email' in str(exc.value)

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_network_error(self, mock_post, brevo_provider, simple_message):
        import requests
        mock_post.side_effect = requests.ConnectionError('Network down')

        with pytest.raises(EmailSendError) as exc:
            brevo_provider.send(simple_message)
        assert 'Failed to send email via Brevo' in str(exc.value)


# =============================================================================
# TEMPLATE EMAIL TESTS
# =============================================================================

class TestBrevoTemplateEmail:
    """Test template email sending."""

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_template_email(self, mock_post, brevo_provider, template_message, mock_response_success):
        mock_post.return_value = mock_response_success

        response = brevo_provider.send(template_message)
        assert response.success is True

        payload = mock_post.call_args[1]['json']
        assert payload['templateId'] == 12
        assert payload['params'] == {'name': 'John Doe', 'company': 'Acme Corp'}

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_template_with_empty_data(self, mock_post, brevo_provider, mock_response_success):
        mock_post.return_value = mock_response_success

        message = EmailMessageDto(
            to='recipient@example.com',
            subject='',
            body='',
            template_id=999,
            template_data=None
        )

        brevo_provider.send(message)
        payload = mock_post.call_args[1]['json']
        assert payload['templateId'] == 999
        assert payload['params'] == {}


# =============================================================================
# BULK EMAIL TESTS
# =============================================================================

class TestBrevoBulkEmail:
    """Test bulk email sending."""

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_bulk_success(self, mock_post, brevo_provider):
        mock_resp = Mock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {'messageId': ['msg1', 'msg2', 'msg3']}
        mock_post.return_value = mock_resp

        messages = [
            EmailMessageDto(to='a@example.com', subject='S1', body='Body1'),
            EmailMessageDto(to='b@example.com', subject='S2', body='Body2'),
            EmailMessageDto(to='c@example.com', subject='S3', body='Body3'),
        ]

        bulk = BulkEmailDTO(messages=messages)
        result = brevo_provider.send_bulk(bulk)

        assert result.total == 3
        assert result.successful == 3
        assert result.failed == 0
        assert mock_post.call_count == 1

    @patch('mailbridge.providers.brevo_provider.requests.post')
    def test_send_bulk_api_error(self, mock_post, brevo_provider):
        mock_resp = Mock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {'code': 'invalid_data', 'message': 'Bad payload'}
        mock_post.return_value = mock_resp

        bulk = BulkEmailDTO(messages=[
            EmailMessageDto(to='a@example.com', subject='S1', body='Body1')
        ])

        with pytest.raises(EmailSendError) as exc:
            brevo_provider.send_bulk(bulk)
        assert 'Brevo API error' in str(exc.value)
        assert 'invalid_data' in str(exc.value)


# =============================================================================
# HELPER TESTS
# =============================================================================

class TestBrevoHelpers:
    """Test helper methods for payload building and attachments."""

    def test_build_payload_regular(self, brevo_provider):
        message = EmailMessageDto(
            to='test@example.com',
            subject='Hi',
            body='Body text',
            html=False
        )
        payload = brevo_provider._build_payload(message)
        assert payload['subject'] == 'Hi'
        assert payload['textContent'] == 'Body text'

    def test_build_payload_template(self, brevo_provider):
        message = EmailMessageDto(
            to='test@example.com',
            template_id=88,
            template_data={'x': 'y'}
        )
        payload = brevo_provider._build_payload(message)
        assert payload['templateId'] == 88
        assert payload['params'] == {'x': 'y'}

    def test_build_attachments(self, brevo_provider, tmp_path):
        file_path = tmp_path / "a.txt"
        file_path.write_text("content")

        result = brevo_provider._build_attachments([file_path])
        assert len(result) == 1
        decoded = base64.b64decode(result[0]['content']).decode()
        assert decoded == 'content'


# =============================================================================
# CONTEXT MANAGER TESTS
# =============================================================================

class TestBrevoContextManager:
    def test_context_manager(self, brevo_config):
        with BrevoProvider(**brevo_config) as provider:
            assert isinstance(provider, BrevoProvider)
        # No cleanup needed, just pattern validation


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
