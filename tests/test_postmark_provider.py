import pytest
from mailbridge.providers.postmark_provider import PostmarkProvider

@pytest.fixture
def postmark_provider():
    return PostmarkProvider(server_token="PM.TEST", endpoint="https://api.postmarkapp.com/email")

def test_send_email_postmark(mocker, postmark_provider):
    mock_post = mocker.patch("requests.post")
    mock_response = mocker.Mock(status_code=200)
    mock_post.return_value = mock_response

    result = postmark_provider.send("to@test.com", "Hi", "<p>Postmark body</p>", "from@test.com")

    assert result is True
    mock_post.assert_called_once_with(
        "https://api.postmarkapp.com/email",
        json=mocker.ANY,
        headers=mocker.ANY
    )
