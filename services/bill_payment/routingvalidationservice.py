from common import connector
from common import environment
import xml.etree.ElementTree as ET
from services.bill_payment.domain import billpayaccountvalidation

PRODUCTION_URL = 'https://api.mastercard.com/billpayAPI/v1/isRoutingValid?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/billpayAPI/v1/isRoutingValid?Format=XML'


class RoutingValidationService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_bill_pay_account_validation(self, bill_pay_account_validation):
        body = self.generate_xml(bill_pay_account_validation)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def generate_xml(self, bill_pay_account_validation):
        el_bill_pay_account_validation = ET.Element('BillPayAccountValidation')
        el_rpps_id = ET.SubElement(el_bill_pay_account_validation, 'RppsId')
        el_rpps_id.text = bill_pay_account_validation.rpps_id
        el_biller_id = ET.SubElement(el_bill_pay_account_validation, "BillerId")
        el_biller_id.text = bill_pay_account_validation.biller_id
        el_account_number = ET.SubElement(el_bill_pay_account_validation, "AccountNumber")
        el_account_number.text = bill_pay_account_validation.account_number
        el_transaction_amount = ET.SubElement(el_bill_pay_account_validation, "TransactionAmount")
        el_transaction_amount.text = bill_pay_account_validation.transaction_amount
        el_customer_identifier_1 = ET.SubElement(el_bill_pay_account_validation, "CustomerIdentifier1")
        el_customer_identifier_1.text = bill_pay_account_validation.customer_identifier_1
        el_customer_identifier_2 = ET.SubElement(el_bill_pay_account_validation, "CustomerIdentifier2")
        el_customer_identifier_2.text = bill_pay_account_validation.customer_identifier_2
        el_customer_identifier_3 = ET.SubElement(el_bill_pay_account_validation, "CustomerIdentifier3")
        el_customer_identifier_3.text = bill_pay_account_validation.customer_identifier_3
        el_customer_identifier_4 = ET.SubElement(el_bill_pay_account_validation, "CustomerIdentifier4")
        el_customer_identifier_4.text = bill_pay_account_validation.customer_identifier_4
        el_response_string = ET.SubElement(el_bill_pay_account_validation, "ResponseString")
        el_response_string.text = bill_pay_account_validation.response_string
        return ET.tostring(el_bill_pay_account_validation, encoding="unicode")

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_return_object(self, xml_response):
        bill_pay_account_validation = billpayaccountvalidation.BillPayAccountValidation()
        bill_pay_account_validation.rpps_id = xml_response.find('RppsId').text
        bill_pay_account_validation.biller_id = xml_response.find('BillerId').text
        bill_pay_account_validation.account_number = xml_response.find('AccountNumber').text
        bill_pay_account_validation.transaction_amount = xml_response.find('TransactionAmount').text
        bill_pay_account_validation.customer_identifier_1 = xml_response.find('CustomerIdentifier1').text
        bill_pay_account_validation.customer_identifier_2 = xml_response.find('CustomerIdentifier2').text
        bill_pay_account_validation.customer_identifier_3 = xml_response.find('CustomerIdentifier3').text
        bill_pay_account_validation.customer_identifier_4 = xml_response.find('CustomerIdentifier4').text
        bill_pay_account_validation.response_string = xml_response.find('ResponseString').text
        return bill_pay_account_validation