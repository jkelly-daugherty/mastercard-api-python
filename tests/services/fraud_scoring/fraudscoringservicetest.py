import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.fraud_scoring import fraudscoringservice
from tests.services.fraud_scoring import matchindicatorstatus
from services.fraud_scoring.domain import scorelookuprequest
from services.fraud_scoring.domain import transactiondetail

transaction_detail = transactiondetail.TransactionDetail()
score_lookup_request = scorelookuprequest.ScoreLookupRequest()

class FraudScoringServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = fraudscoringservice.FraudScoringService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                test_utils.get_private_key(),
                                                                environment.Environment.SANDBOX)
        transaction_detail.customer_identifier = '1996'
        transaction_detail.merchant_identifier = '123'
        transaction_detail.account_number = '5555555555555555555'
        transaction_detail.account_prefix = '555555'
        transaction_detail.account_suffix = '5555'
        transaction_detail.transaction_date = '1231'
        transaction_detail.transaction_time = '035959'
        transaction_detail.bank_net_reference_number = 'abcABC123'
        transaction_detail.stan = '123456'

    def test_low_fraud_scoring_single_transaction_match(self):
        transaction_detail.transaction_amount = '62500'
        score_lookup_request.transaction_detail = transaction_detail
        score_lookup = self._service.get_score_lookup(score_lookup_request)
        assert score_lookup.score_response.match_indicator == matchindicatorstatus.MatchIndicatorStatus.SINGLE_TRANSACTION_MATCH

    def test_mid_fraud_scoring_single_transaction_match(self):
        transaction_detail.transaction_amount = '10001'
        score_lookup_request.transaction_detail = transaction_detail
        score_lookup = self._service.get_score_lookup(score_lookup_request)
        assert score_lookup.score_response.match_indicator == matchindicatorstatus.MatchIndicatorStatus.MULTIPLE_TRANS_IDENTICAL_CARD_MATCH

    def test_high_fraud_scoring_single_transaction_match(self):
        transaction_detail.transaction_amount = '20001'
        score_lookup_request.transaction_detail = transaction_detail
        score_lookup = self._service.get_score_lookup(score_lookup_request)
        assert score_lookup.score_response.match_indicator == matchindicatorstatus.MatchIndicatorStatus.MULTIPLE_TRANS_DIFFERING_CARDS_MATCH

    def test_no_match_found(self):
        transaction_detail.transaction_amount = '30001'
        score_lookup_request.transaction_detail = transaction_detail
        score_lookup = self._service.get_score_lookup(score_lookup_request)
        assert score_lookup.score_response.match_indicator == matchindicatorstatus.MatchIndicatorStatus.NO_MATCH_FOUND

    def test_system_error(self):
        transaction_detail.transaction_amount = '50001'
        score_lookup_request.transaction_detail = transaction_detail
        try:
            score_lookup = self._service.get_score_lookup(score_lookup_request)
        except BaseException as err:
            print('Expected exception: {0}'.format(err))
        else:
            print('Test failure. Expected an exception.')