import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.moneysend.services import cardmappingservice
from services.moneysend.domain.card_mapping import createmappingrequest
from services.moneysend.domain.card_mapping import inquiremappingrequest
from services.moneysend.domain.card_mapping import updatemappingrequest
from services.moneysend.domain.options import deletemappingrequestoptions
from services.moneysend.domain.options import updatemappingrequestoptions
from services.moneysend.domain.common import address
from services.moneysend.domain.common import cardholderfullname


class CardMappingServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = cardmappingservice.CardMappingService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_create_mapping(self):
        create_mapping_request = createmappingrequest.CreateMappingRequest()
        create_mapping_request.subscriber_id = 'examplePythonReceiving9@email.com'
        create_mapping_request.subscriber_type = 'EMAIL_ADDRESS'
        create_mapping_request.account_usage = 'RECEIVING'
        create_mapping_request.account_number = '5184680430000014'
        create_mapping_request.default_indicator = 'T'
        create_mapping_request.expiry_date = '201409'
        create_mapping_request.alias = 'My Debit Card'
        create_mapping_request.ica = '009674'

        tmp_address = address.Address()
        tmp_address.line1 = '123 Main Street'
        tmp_address.line2 = '#5A'
        tmp_address.city = 'OFallon'
        tmp_address.country_subdivision = 'MO'
        tmp_address.country = 'USA'
        tmp_address.postal_code = '63368'

        tmp_cardholder_full_name = cardholderfullname.CardholderFullName()
        tmp_cardholder_full_name.cardholder_first_name = 'John'
        tmp_cardholder_full_name.cardholder_middle_name = 'Q'
        tmp_cardholder_full_name.cardholder_last_name = 'Public'

        create_mapping_request.address = tmp_address
        create_mapping_request.cardholder_full_name = tmp_cardholder_full_name
        create_mapping_request.date_of_birth = '19460102'

        create_mapping = self._service.get_create_mapping(create_mapping_request)
        assert create_mapping.request_id is not None and int(create_mapping.request_id) > 0
        assert create_mapping.mapping.mapping_id is not None and int(create_mapping.mapping.mapping_id) > 0

    def test_inquire_mapping_one_mapping(self):
        inquire_mapping_request = inquiremappingrequest.InquireMappingRequest()
        inquire_mapping_request.subscriber_id = 'examplePythonReceiving7@email.com'
        inquire_mapping_request.subscriber_type = 'EMAIL_ADDRESS'
        inquire_mapping_request.account_usage = 'RECEIVING'
        inquire_mapping_request.alias = 'My Debit Card'
        inquire_mapping_request.data_response_flag = '1'
        inquire_mapping = self._service.get_inquire_mapping(inquire_mapping_request)
        assert inquire_mapping is not None
        assert inquire_mapping.request_id is not None and int(inquire_mapping.request_id) > 0
        assert inquire_mapping.mappings.mapping[0].mapping_id is not None\
               and int(inquire_mapping.mappings.mapping[0].mapping_id) > 0

    def test_inquire_mapping_mappings(self):
        inquire_mapping_request = inquiremappingrequest.InquireMappingRequest()
        inquire_mapping_request.subscriber_id = 'examplePythonReceiving7@email.com'
        inquire_mapping_request.subscriber_type = 'EMAIL_ADDRESS'
        inquire_mapping = self._service.get_inquire_mapping(inquire_mapping_request)
        assert inquire_mapping is not None
        assert inquire_mapping.request_id is not None and int(inquire_mapping.request_id) > 0
        assert inquire_mapping.mappings.mapping[0].mapping_id is not None\
               and int(inquire_mapping.mappings.mapping[0].mapping_id) > 0

    def test_update_mapping(self):
        inquire_mapping_request = inquiremappingrequest.InquireMappingRequest()
        inquire_mapping_request.subscriber_id = 'examplePythonReceiving7@email.com'
        inquire_mapping_request.subscriber_type = 'EMAIL_ADDRESS'
        inquire_mapping = self._service.get_inquire_mapping(inquire_mapping_request)
        assert inquire_mapping is not None
        assert inquire_mapping.request_id is not None and int(inquire_mapping.request_id) > 0
        assert inquire_mapping.mappings.mapping[0].mapping_id is not None \
            and int(inquire_mapping.mappings.mapping[0].mapping_id) > 0
        update_mapping_request = updatemappingrequest.UpdateMappingRequest()
        update_mapping_request_options = \
            updatemappingrequestoptions.UpdateMappingRequestOptions(inquire_mapping.mappings.mapping[0].mapping_id)
        update_mapping_request.account_usage = 'RECEIVING'
        update_mapping_request.account_number = '5184680430000014'
        update_mapping_request.default_indicator = 'T'
        update_mapping_request.expiry_date = '201409'
        update_mapping_request.alias = 'Updated Debit Card'

        tmp_address = address.Address()
        tmp_address.line1 = '123 Main Street'
        tmp_address.line2 = '#5A'
        tmp_address.city = 'OFallon'
        tmp_address.country_subdivision = 'MO'
        tmp_address.country = 'USA'
        tmp_address.postal_code = '63368'

        tmp_cardholder_full_name = cardholderfullname.CardholderFullName()
        tmp_cardholder_full_name.cardholder_first_name = 'Johnny'
        tmp_cardholder_full_name.cardholder_middle_name = 'X'
        tmp_cardholder_full_name.cardholder_last_name = 'Public'

        update_mapping_request.address = tmp_address
        update_mapping_request.cardholder_full_name = tmp_cardholder_full_name
        update_mapping_request.date_of_birth = '19460102'
        update_mapping = self._service.get_update_mapping(update_mapping_request, update_mapping_request_options)
        assert update_mapping.request_id is not None and int(update_mapping.request_id) > 0
        assert update_mapping.mapping.mapping_id is not None and int(update_mapping.mapping.mapping_id) > 0

    def test_delete_mapping(self):
        inquire_mapping_request = inquiremappingrequest.InquireMappingRequest()
        inquire_mapping_request.subscriber_id = 'examplePythonReceiving7@email.com'
        inquire_mapping_request.subscriber_type = 'EMAIL_ADDRESS'
        inquire_mapping = self._service.get_inquire_mapping(inquire_mapping_request)
        assert inquire_mapping is not None
        assert inquire_mapping.request_id is not None and int(inquire_mapping.request_id) > 0
        assert inquire_mapping.mappings.mapping[0].mapping_id is not None \
            and int(inquire_mapping.mappings.mapping[0].mapping_id) > 0
        delete_mapping_request_options = \
            deletemappingrequestoptions.DeleteMappingRequestOptions(inquire_mapping.mappings.mapping[0].mapping_id)
        delete_mapping = self._service.get_delete_mapping(delete_mapping_request_options)
        assert delete_mapping is not None
        assert delete_mapping.request_id is not None and int(delete_mapping.request_id) > 0
        assert delete_mapping.mapping.mapping_id is not None and int(delete_mapping.mapping.mapping_id) > 0