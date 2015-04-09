import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.lost_stolen import loststolenservice


class LostStolenServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = loststolenservice.LostStolenService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_stolen(self):
        account = self._service.get_account('5343434343434343')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'S'
        assert account.reason == 'STOLEN'

    def test_fraud(self):
        account = self._service.get_account('5105105105105100')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'F'
        assert account.reason == 'FRAUD'

    def test_lost(self):
        account = self._service.get_account('5222222222222200')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'L'
        assert account.reason == 'LOST'

    def test_capture_card(self):
        account = self._service.get_account('5305305305305300')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'P'
        assert account.reason == 'CAPTURE CARD'

    def test_capture_unauthorized_use(self):
        account = self._service.get_account('6011111111111117')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'U'
        assert account.reason == 'UNAUTHORIZED USE'

    def test_counterfeit(self):
        account = self._service.get_account('4444333322221111')
        assert account.status == 'true'
        assert account.listed == 'true'
        assert account.reason_code == 'X'
        assert account.reason == 'COUNTERFEIT'

    def test_not_listed(self):
        account = self._service.get_account('343434343434343')
        assert account.status == 'true'
        assert account.listed == 'false'
        self.assertEqual(account.reason_code, None)
        self.assertEqual(account.reason, None)