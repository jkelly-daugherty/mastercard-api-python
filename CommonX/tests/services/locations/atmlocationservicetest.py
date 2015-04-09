import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.locations.atms.services import atmlocationservice
from services.locations.domain.options.atms import atmlocationrequestoptions


class AtmLocationServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = atmlocationservice.AtmLocationService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                              test_utils.get_private_key(),
                                                              environment.Environment.SANDBOX)

    def test_by_numeric_postal_code(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.country = 'USA'
        options.postal_code = '46320'
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_foreign_postal_code(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.country = 'SGP'
        options.postal_code = '068897'
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_latitude_longitude(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.latitude = '1.2833'
        options.longitude = '103.8499'
        options.radius = 5
        options.distance_unit = atmlocationrequestoptions.AtmLocationRequestOptions.KILOMETER
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_address(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.address_line1 = 'BLK 1 ROCHOR ROAD UNIT 01-640 ROCHOR ROAD'
        options.country = 'SGP'
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_city(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.city = 'CHICAGO'
        options.country = 'USA'
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_country_subdivision(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.country = 'USA'
        options.country_subdivision = 'IL'
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0

    def test_by_support_emv(self):
        options = atmlocationrequestoptions.AtmLocationRequestOptions(0, 25)
        options.support_emv = atmlocationrequestoptions.AtmLocationRequestOptions.SUPPORT_EMV_YES
        options.latitude = 1.2833
        options.longitude = 103.8499
        atms_ = self._service.get_atms(options)
        assert atms_.atm is not None
        assert len(atms_.atm) > 0