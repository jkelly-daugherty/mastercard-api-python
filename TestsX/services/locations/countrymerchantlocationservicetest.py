import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.merchants.services import countrymerchantlocationservice
from services.locations.domain.options.merchants import countrymerchantlocationrequestoptions
from services.locations.domain.options.merchants import details


class CountryMerchantLocationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = countrymerchantlocationservice.CountryMerchantLocationService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                            test_utils.get_private_key(),
                                                                            environment.Environment.SANDBOX)

    def test_country_merchant_location_service(self):
        options = countrymerchantlocationrequestoptions.CountryMerchantLocationRequestOptions(details.Details.ACCEPTANCE_PAYPASS)
        countries = self._service.get_countries(options)
        assert countries is not None
        assert len(countries.country) > 0