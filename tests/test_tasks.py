import sys
from nose.tools import assert_true, assert_false, assert_equal, assert_raises, nottest
try:
    from unittest.mock import MagicMock, Mock, patch
except ImportError:
    from mock import MagicMock, Mock, patch

from emailq.tasks.tasks import sendmail
import smtplib
from celery.exceptions import MaxRetriesExceededError


@patch('emailq.tasks.tasks.smtplib.SMTP')
def test_sendmail(mock_SMTP):
    to = 'test@test.com'
    subject = 'test'
    body = 'test'
    mock_SMTP.return_value = Mock()
    assert_true(sendmail(to=to,subject=subject,body=body))

