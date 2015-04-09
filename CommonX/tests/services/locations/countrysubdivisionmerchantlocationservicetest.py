import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.merchants.services import countrysubdivisionmerchantlocationservice
from services.locations.domain.options.merchants import countrysubdivisionmerchantlocationrequestoptions
from services.locations.domain.options.merchants import details


class CountrySubdivisionMerchantLocationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = countrysubdivisionmerchantlocationservice.CountrySubdivisionMerchantLocationService(
                                                                    testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                    test_utils.get_private_key(),
                                                                    environment.Environment.SANDBOX)

    def test_country_subdivision_service_with_paypass(self):
        options = countrysubdivisionmerchantlocationrequestoptions.CountrySubdivisionMerchantLocationRequestOptions(
                                                                            details.Details.ACCEPTANCE_PAYPASS, 'USA')
        country_subdivisions = self._service.get_country_subdivisions(options)
        assert country_subdivisions is not None
        assert len(country_subdivisions.country_subdivision) > 0

    def test_country_subdivision_service_with_offers(self):
        options = countrysubdivisionmerchantlocationrequestoptions.CountrySubdivisionMerchantLocationRequestOptions(
                                                                            details.Details.OFFERS_EASYSAVINGS, 'USA')
        country_subdivisions = self._service.get_country_subdivisions(options)
        assert country_subdivisions is not None
        assert len(country_subdivisions.country_subdivision) > 0

    def test_country_subdivision_service_with_prepaid_travel(self):
        options = countrysubdivisionmerchantlocationrequestoptions.CountrySubdivisionMerchantLocationRequestOptions(
                                                                            details.Details.PRODUCTS_PREPAID_TRAVEL_CARD, 'USA')
        country_subdivisions = self._service.get_country_subdivisions(options)
        assert country_subdivisions is not None
        assert len(country_subdivisions.country_subdivision) > 0

    def test_country_subdivision_service_with_repower(self):
        options = countrysubdivisionmerchantlocationrequestoptions.CountrySubdivisionMerchantLocationRequestOptions(
                                                                            details.Details.TOPUP_REPOWER, 'USA')
        country_subdivisions = self._service.get_country_subdivisions(options)
        assert country_subdivisions is not None
        assert len(country_subdivisions.country_subdivision) > 0