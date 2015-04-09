from common import connector
from common import urlutil
from common import environment
import xml.etree.ElementTree as ET
from services.moneysend.domain.card_mapping import deletesubscriberid
from services.moneysend.domain.card_mapping import deletesubscriberidrequest

PRODUCTION_URL = 'https://api.mastercard.com/moneysend/v2/mapping/subscriber?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/moneysend/v2/mapping/subscriber?Format=XML'


class DeleteSubscriberIdService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_delete_subscriber_id(self, delete_subscriber_id_request):
        body = self.generate_xml(delete_subscriber_id_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def get_url(self, options=None):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_xml(self, delete_subscriber_id_request):
        el_delete_subscriber_id_request = ET.Element('DeleteSubscriberIdRequest')
        el_subscriber_id = ET.SubElement(el_delete_subscriber_id_request, 'SubscriberId')
        el_subscriber_id.text = delete_subscriber_id_request.subscriber_id
        el_subscriber_type = ET.SubElement(el_delete_subscriber_id_request, 'SubscriberType')
        el_subscriber_type.text = delete_subscriber_id_request.subscriber_type
        return ET.tostring(el_delete_subscriber_id_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        delete_subscriber_id = deletesubscriberid.DeleteSubscriberId()
        delete_subscriber_id.request_id = xml_response.find('RequestId').text
        return delete_subscriber_id