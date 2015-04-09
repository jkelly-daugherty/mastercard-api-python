import unittest
from tests import testutils
from common import environment
from tests import testconstants
from services.moneysend.services import deletesubscriberidservice
from services.moneysend.domain.card_mapping import deletesubscriberidrequest


class DeleteSubscriberIdServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = deletesubscriberidservice.DeleteSubscriberIdService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                            test_utils.get_private_key(),
                                                            environment.Environment.SANDBOX)

    def test_delete_subscriber_id_service(self):
        delete_subscriber_id_request = deletesubscriberidrequest.DeleteSubscriberIdRequest()
        delete_subscriber_id_request.subscriber_id = 'examplePythonReceiving3@email.com'
        delete_subscriber_id_request.subscriber_type = 'EMAIL_ADDRESS'
        delete_subscriber_id = self._service.get_delete_subscriber_id(delete_subscriber_id_request)
        assert delete_subscriber_id is not None
        assert delete_subscriber_id.request_id is not None and int(delete_subscriber_id.request_id) > 0