from common import connector
from common import environment
import xml.etree.ElementTree as ET
from services.lost_stolen.domain import account

PRODUCTION_URL = 'https://api.mastercard.com/fraud/loststolen/v1/account-inquiry?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/fraud/loststolen/v1/account-inquiry?Format=XML'


class LostStolenService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_account(self, account_number):
        body = self.generate_xml(account_number)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def generate_xml(self, account_number):
        el_account_inquiry = ET.Element('AccountInquiry')
        el_account_number = ET.SubElement(el_account_inquiry, 'AccountNumber')
        el_account_number.text = account_number
        return ET.tostring(el_account_inquiry, encoding="unicode")

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_return_object(self, xml_response):
        returned_account = account.Account()
        returned_account.status = xml_response.find('Status').text
        returned_account.listed = xml_response.find('Listed').text
        returned_account.reason_code = xml_response.find('ReasonCode').text
        returned_account.reason = xml_response.find('Reason').text
        return returned_account