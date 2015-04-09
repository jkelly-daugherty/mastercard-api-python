import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.match.services import terminationinquiryservice
from services.match.domain import principaltype
from services.match.domain import driverslicensetype
from services.match.domain import addresstype
from services.match.domain import merchanttype
from services.match.domain import terminationinquiryrequest
from services.match.domain.options import terminationinquiryrequestoptions

class TerminationInquiryServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = terminationinquiryservice.TerminationInquiryService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                            test_utils.get_private_key(),
                                                                            environment.Environment.SANDBOX)

    def test_termination_inquiry(self):
        principal_address = addresstype.AddressType()
        principal_address.line1 = '93-52 243 STREET'
        principal_address.city = 'BELLEROSE'
        principal_address.country_subdivision = 'NY'
        principal_address.country = 'USA'
        principal_address.postal_code = '55555-5555'
        principal = principaltype.PrincipalType()
        principal.first_name = 'PATRICIA'
        principal.last_name = 'CLARKE'
        principal.address = principal_address
        principal_drivers_license = driverslicensetype.DriversLicenseType()
        principal_drivers_license.number = ''
        principal_drivers_license.country = ''
        principal_drivers_license.country_subdivision = ''
        principal.drivers_license = principal_drivers_license
        merchant_address = addresstype.AddressType()
        merchant_address.line1 = '20 EAST MAIN ST'
        merchant_address.line2 = 'EAST ISLIP           NY'
        merchant_address.city = 'EAST ISLIP'
        merchant_address.country_subdivision = 'NY'
        merchant_address.country = 'USA'
        merchant_address.postal_code = '55555'
        merchant = merchanttype.MerchantType()
        merchant.address = merchant_address
        merchant.country_subdivision_tax_id = '205545287'
        merchant.national_tax_id = '2891327625'
        merchant.name = 'TERMINATED MERCHANT 2'
        merchant.doing_business_as_name = 'DOING BUSINESS AS TERMINATED MERCHANT 2'
        merchant.phone_number = '5555555555'
        merchant.principal = principal
        request = terminationinquiryrequest.TerminationInquiryRequest()
        request.acquirer_id = '1996'
        request.merchant = merchant
        request.transaction_reference_number = '12345'
        response = self._service.get_termination_inquiry(request, terminationinquiryrequestoptions.TerminationInquiryRequestOptions(0, 10))
        assert response.transaction_reference_number is not None
        assert response.terminated_merchant is not None
        assert response.terminated_merchant[0].termination_reason_code is not None
        assert response.terminated_merchant[0].merchant.name is not None