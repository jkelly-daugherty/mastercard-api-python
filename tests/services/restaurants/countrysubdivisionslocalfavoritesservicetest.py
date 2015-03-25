import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.restaurants.services import countrysubdivisionslocalfavoritesservice
from services.restaurants.domain.options import countrysubdivisionslocalfavoritesrequestoptions


class CountrySubdivisionsLocalFavoritesServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = countrysubdivisionslocalfavoritesservice.CountrySubdivisionsLocalFavoritesService(
                                                                    testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                    test_utils.get_private_key(),
                                                                    environment.Environment.SANDBOX)

    def test_country_subdivision_service(self):
        options = countrysubdivisionslocalfavoritesrequestoptions.CountrySubdivisionsLocalFavoritesRequestOptions('USA')
        country_subdivisions = self._service.get_country_subdivisions(options)
        assert country_subdivisions is not None
        assert len(country_subdivisions.country_subdivision) > 0