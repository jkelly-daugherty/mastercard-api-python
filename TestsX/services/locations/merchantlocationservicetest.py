import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.merchants.services import merchantlocationservice
from services.locations.domain.options.merchants import merchantlocationrequestoptions
from services.locations.domain.common.countries import country
from services.locations.domain.options.merchants import details


class MerchantLocationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.PRODUCTION)
        self._service = merchantlocationservice.MerchantLocationService(testconstants.TestConstants.PRODUCTION_CONSUMER_KEY,
                                                                        test_utils.get_private_key(),
                                                                        environment.Environment.PRODUCTION)

    def test_merchant_location_service_repower(self):
        options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.TOPUP_REPOWER, 0, 25)
        country_ = country.Country('USA', '')
        options.country = country_
        options.postal_code = '22122'
        merchants = self._service.get_merchants(options)
        assert int(merchants.merchant[0].id) > 0
        assert len(merchants.merchant) > 0

    # At the time of the creation of this SDK, PPTC was not returning
    # valid results. Passing of this test implies that PPTC has begun to return
    # valid results and that no SDK changes are needed.

    # def test_merchant_location_service_prepaid_travel_card_fail(self):
    #     options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.PRODUCTS_PREPAID_TRAVEL_CARD, 0, 25)
    #     country_ = country.Country('USA', '')
    #     options.country = country_
    #     options.postal_code = '20006'
    #     merchants = self._service.get_merchants(options)
    #     assert int(merchants.merchant[0].id) > 0
    #     assert len(merchants.merchant) > 0

    # At the time of the creation of this SDK, PPTC was not returning valid results
    # Comment out this unit test once it does.

    def test_merchant_location_service_prepaid_travel_card_pass(self):
        options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.PRODUCTS_PREPAID_TRAVEL_CARD, 0, 25)
        country_ = country.Country('USA', '')
        options.country = country_
        options.postal_code = '20006'
        merchants = self._service.get_merchants(options)
        assert int(merchants.merchant[0].id) is None
        assert len(merchants.merchant) == 0

    def test_merchant_location_service_offers(self):
        options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.OFFERS_EASYSAVINGS, 0, 25)
        country_ = country.Country('USA', '')
        options.country = country_
        options.postal_code = '22122'
        merchants = self._service.get_merchants(options)
        assert int(merchants.merchant[0].id) > 0
        assert len(merchants.merchant) > 0

    def test_merchant_location_service_paypass(self):
        options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.ACCEPTANCE_PAYPASS, 0, 25)
        country_ = country.Country('USA', '')
        options.country = country_
        options.postal_code = '07032'
        merchants = self._service.get_merchants(options)
        assert int(merchants.merchant[0].id) > 0
        assert len(merchants.merchant) > 0

    def test_merchant_location_service_cashback(self):
        options = merchantlocationrequestoptions.MerchantLocationRequestOptions(details.Details.FEATURES_CASHBACK, 0, 25)
        country_ = country.Country('USA', '')
        options.country = country_
        options.postal_code = '46323'
        merchants = self._service.get_merchants(options)
        assert int(merchants.merchant[0].id) > 0
        assert len(merchants.merchant) > 0