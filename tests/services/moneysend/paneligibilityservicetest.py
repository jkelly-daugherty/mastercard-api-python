import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.moneysend.services import paneligibilityservice
from services.moneysend.domain.pan_eligibility import paneligibilityrequest


class PanEligibilityServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = paneligibilityservice.PanEligibilityService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_pan_eligibility_service_eligible(self):
        pan_eligibility_request = paneligibilityrequest.PanEligibilityRequest()
        pan_eligibility_request.sending_account_number = '5184680430000006'
        pan_eligibility_request.receiving_account_number = '5184680430000006'
        pan_eligibility = self._service.get_pan_eligibility(pan_eligibility_request)
        assert pan_eligibility is not None
        assert pan_eligibility.sending_eligibility.eligible == 'true'
        assert pan_eligibility.receiving_eligibility.eligible == 'true'

    def test_pan_eligibility_service_sending_not_eligible(self):
        pan_eligibility_request = paneligibilityrequest.PanEligibilityRequest()
        pan_eligibility_request.sending_account_number = '5184680990000024'
        pan_eligibility = self._service.get_pan_eligibility(pan_eligibility_request)
        assert pan_eligibility is not None
        assert pan_eligibility.sending_eligibility.eligible == 'false'

    def test_pan_eligibility_service_receiving_not_eligible(self):
        pan_eligibility_request = paneligibilityrequest.PanEligibilityRequest()
        pan_eligibility_request.receiving_account_number = '5184680060000201'
        pan_eligibility = self._service.get_pan_eligibility(pan_eligibility_request)
        assert pan_eligibility is not None
        assert pan_eligibility.receiving_eligibility.eligible == 'false'