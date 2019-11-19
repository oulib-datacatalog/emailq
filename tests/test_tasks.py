import sys
from nose.tools import assert_true, assert_false, assert_equal, nottest
try:
    from unittest.mock import MagicMock, Mock, patch
except ImportError:
    from mock import MagicMock, Mock, patch

from emailq.tasks.tasks import sendmail
