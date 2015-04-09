import unittest
import random
from tests import testutils
from common import environment
from tests import testconstants
from services.repower.repower import repowerservice
from services.repower.repower.domain import repowerrequest
from services.repower.repower.domain import transactionamount
from services.repower.repower.domain import cardacceptor
from services.repower.repower_reversal import repowerreversalservice
from services.repower.repower_reversal.domain import repowerreversalrequest


class RepowerServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = repowerservice.RepowerService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                      test_utils.get_private_key(),
                                                      environment.Environment.SANDBOX)
        self._service_reversal = repowerreversalservice.RepowerReversalService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                               test_utils.get_private_key(),
                                                                               environment.Environment.SANDBOX)

    def test_repower_service(self):
        trans_ref = self.trans_ref_num(19)

        repower_request = repowerrequest.RepowerRequest()
        repower_request.transaction_reference = trans_ref
        repower_request.card_number = '5184680430000014'

        transaction_amount = transactionamount.TransactionAmount()
        transaction_amount.value = '000000030000'
        transaction_amount.currency = '840'
        repower_request.transaction_amount = transaction_amount

        repower_request.local_date = '1230'
        repower_request.local_time = '092435'
        repower_request.channel = 'W'
        repower_request.ica = '009674'
        repower_request.processor_id = '9000000442'
        repower_request.routing_and_transit_number = '990442082'
        repower_request.merchant_type = '6532'

        card_acceptor = cardacceptor.CardAcceptor()
        card_acceptor.name = 'Prepaid Load Store'
        card_acceptor.city = 'St Charles'
        card_acceptor.state = 'MO'
        card_acceptor.postal_code = '63301'
        card_acceptor.country = 'USA'
        repower_request.card_acceptor = card_acceptor

        repower = self._service.get_repower(repower_request)
        assert repower.request_id is not None
        assert int(repower.request_id) > 0
        assert int(repower.transaction_history.transaction.response.code) == 00

        repower_reversal_request = repowerreversalrequest.RepowerReversalRequest()
        repower_reversal_request.ica = '009674'
        repower_reversal_request.reversal_reason = 'UNIT TEST'
        repower_reversal_request.transaction_reference = trans_ref

        repower_reversal = self._service_reversal.get_repower_reversal(repower_reversal_request)
        assert repower_reversal.request_id is not None
        assert int(repower_reversal.transaction_history.transaction.response.code) == 00

    def trans_ref_num(self, x, leading_zeroes=True):
        if not leading_zeroes:
            return random.randint(10**(x-1), 10**x-1)
        else:
            if x > 6000:
                return ''.join([str(random.randint(0, 9)) for i in range(x)])
            else:
                return str("%0." + str(x) + "d") % random.randint(0, 10**x-1)