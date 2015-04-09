import unittest
import random
from tests import testutils
from common import environment
from tests import testconstants
from services.moneysend.services import transferreversalservice
from services.moneysend.domain.transfer import transferreversalrequest


class TransferReversalServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = transferreversalservice.TransferReversalService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                        test_utils.get_private_key(),
                                                        environment.Environment.SANDBOX)

    def test_transfer_reversal_request(self):
        transfer_reversal_request = transferreversalrequest.TransferReversalRequest()
        transfer_reversal_request.ica = '009674'
        transfer_reversal_request.transaction_reference = '1250795528251450229'
        transfer_reversal_request.reversal_reason = 'FAILURE IN PROCESSING'

        transfer_reversal = self._service.get_transfer_reversal(transfer_reversal_request)
        assert transfer_reversal.transaction_reference is not None and int(transfer_reversal.transaction_reference) > 0
        assert transfer_reversal.transaction_history.transaction[0] is not None
        assert int(transfer_reversal.transaction_history.transaction[0].response.code) == 00

    def trans_ref_num(self, x, leading_zeroes=True):
        if not leading_zeroes:
            return random.randint(10**(x-1), 10**x-1)
        else:
            if x > 6000:
                return ''.join([str(random.randint(0, 9)) for i in range(x)])
            else:
                return str("%0." + str(x) + "d") % random.randint(0, 10**x-1)