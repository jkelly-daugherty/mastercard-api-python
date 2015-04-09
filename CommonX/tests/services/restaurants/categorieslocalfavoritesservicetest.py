import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.restaurants.services import categorieslocalfavoritesservice


class CategoriesLocalFavoritesServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = categorieslocalfavoritesservice.CategoriesLocalFavoritesService(
                                                                    testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                    test_utils.get_private_key(),
                                                                    environment.Environment.SANDBOX)

    def test_restaurant_categories(self):
        categories = self._service.get_categories()
        assert categories is not None
        assert len(categories.category) > 0