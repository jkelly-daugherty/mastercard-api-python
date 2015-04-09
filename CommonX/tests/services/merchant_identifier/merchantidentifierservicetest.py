import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.merchant_identifier import merchantidentifierservice
from services.merchant_identifier.domain import requestoptions


class MerchantIdentifierServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = merchantidentifierservice.MerchantIdentifierService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_merchant_exact_match(self):
        options = requestoptions.RequestOptions()
        options.merchant_id = 'DIRECTSATELLITETV'
        options.type = 'ExactMatch'
        merchant_ids = self._service.get_merchant_ids(options)
        assert merchant_ids.message is not None
        assert merchant_ids.returned_merchants is not None

    def test_merchant_fuzzy_match(self):
        options = requestoptions.RequestOptions()
        options.merchant_id = 'DIRECTSATELLITETV'
        options.type = 'FuzzyMatch'
        merchant_ids = self._service.get_merchant_ids(options)
        assert merchant_ids.message is not None
        assert merchant_ids.returned_merchants is not None