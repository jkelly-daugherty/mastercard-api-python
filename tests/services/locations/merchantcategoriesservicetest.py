import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.merchants.services import merchantcategoriesservice


class MerchantCategoriesServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = merchantcategoriesservice.MerchantCategoryService(
                                                                    testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                                    test_utils.get_private_key(),
                                                                    environment.Environment.SANDBOX)

    def test_merchant_categories(self):
        categories = self._service.get_categories()
        assert categories is not None
        assert len(categories.category) > 0