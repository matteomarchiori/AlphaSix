from unittest.mock import patch, MagicMock

from pytest import raises

from webhook.gitlab.factory import GitlabWebhookFactory


@patch('webhook.gitlab.factory.GitlabIssueWebhook')
def test_create_webhook(webhook_mock):

    factory = GitlabWebhookFactory()
    webhook = factory.create_webhook('issue')

    webhook_mock.assert_called_once()
    assert isinstance(webhook, MagicMock)

    with raises(NameError):
        factory.create_webhook('aaaa')
