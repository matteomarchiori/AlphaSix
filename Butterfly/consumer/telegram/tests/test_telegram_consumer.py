from unittest.mock import MagicMock, patch

import pytest

from consumer.telegram.consumer import TelegramConsumer


msg = {
    'app': 'gitlab',
    'object_kind': 'issue',
    'receiver': '42',
    'project_name': 'Project',
    'project_id': 'http://...',
    'author': 'author',
    'title': 'Title',
    'description': 'Descriptionz',
    'action': 'open',
}


# @pytest.mark.skip()
def test_format():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock)

    res = consumer.format(msg)

    assert 'Gitlab' in res
    assert 'Project' in res
    assert 'http://...' in res
    assert 'author' in res
    assert 'Descriptionz' in res
    assert '*Description:*' in res
    assert 'testo non presente' not in res


@patch('consumer.telegram.consumer.requests', autospec=True)
# @pytest.mark.skip()
def test_send(requests):
    kafka_mock = MagicMock()
    kafka_mock.subscription.return_value = ['telegram']
    consumer = TelegramConsumer(kafka_mock)

    assert consumer.topics() == ['telegram']

    mock = MagicMock()
    requests.post.return_value = mock
    mock.ok = True
    mock.json.return_value = {
        'result': {
            'chat': {
                'username': 'aaa',
                'id': '123',
            }
        }
    }

    response = consumer.send('123123', msg)
    assert response is True

    mock.json.assert_called_once()

    mock.ok = False
    response = consumer.send('123', msg)
    assert response is False


# @pytest.mark.skip()
def test_listen():
    kafka_mock = MagicMock()
    consumer = TelegramConsumer(kafka_mock)

    kafka_mock.__iter__.return_value = [
        {b'value': b'lul'},
        {b'', b''},
    ]
