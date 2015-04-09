import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.restaurants.services import restaurantslocalfavoritesservice
from services.restaurants.domain.options import restaurantslocalfavoritesrequestoptions


class RestaurantsLocalFavoritesServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = restaurantslocalfavoritesservice.RestaurantLocalFavoritesService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                              test_utils.get_private_key(),
                                                              environment.Environment.SANDBOX)

    def test_by_latitude_longitude(self):
        options = restaurantslocalfavoritesrequestoptions.RestaurantsLocalFavoritesRequestOptions(0, 25)
        options.latitude = '38.53463'
        options.longitude = '-90.286781'
        restaurants_ = self._service.get_restaurants(options)
        assert restaurants_.restaurant is not None
        assert len(restaurants_.restaurant) > 0