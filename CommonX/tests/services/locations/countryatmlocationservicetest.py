import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.atms.services import countryatmlocationservice


class CountryAtmLocationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = countryatmlocationservice.CountryAtmLocationService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                            test_utils.get_private_key(),
                                                                            environment.Environment.SANDBOX)

    def test_country_atm_location_service(self):
        countries = self._service.get_countries()
        assert countries is not None
        assert len(countries.country) > 0