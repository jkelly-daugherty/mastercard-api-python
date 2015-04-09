import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.bill_payment import routingvalidationservice
from services.bill_payment.domain import billpayaccountvalidation


class RoutingValidationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = routingvalidationservice.RoutingValidationService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_routing_validation_service_success(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '99887761'
        bill_pay_account_validation_request.biller_id = '9998887771'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '250.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == "Successful"

    def test_routing_validation_service_invalid_rppsid(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '00000000'
        bill_pay_account_validation_request.biller_id = '9998887771'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '250.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == 'Invalid RPPSID'

    def test_routing_validation_service_inactive_rppisd(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '99887760'
        bill_pay_account_validation_request.biller_id = '9998887771'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '250.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == 'RPPSID is not active'

    def test_routing_validation_service_invalid_billerid(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '99887761'
        bill_pay_account_validation_request.biller_id = '0000000000'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '250.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == 'Invalid BillerID'

    def test_routing_validation_service_inactive_billerid(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '99887761'
        bill_pay_account_validation_request.biller_id = '9998887772'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '250.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == 'BillerID is not active'

    def test_routing_validation_service_exceeds_trans_amount(self):
        bill_pay_account_validation_request = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation_request.rpps_id = '99887761'
        bill_pay_account_validation_request.biller_id = '9998887771'
        bill_pay_account_validation_request.account_number = '1234567890'
        bill_pay_account_validation_request.transaction_amount = '5000.00'
        bill_pay_account_validation_response = self._service.get_bill_pay_account_validation(bill_pay_account_validation_request)
        assert bill_pay_account_validation_response.response_string == 'Transaction Amount exceeds BillerID maximum'