from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.repower.repower.domain import repower
from services.repower.repower.domain import transactionhistory
from services.repower.repower.domain import transaction
from services.repower.repower.domain import response
from services.repower.repower.domain import accountbalance

PRODUCTION_URL = 'https://api.mastercard.com/repower/v1/repower?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/repower/v1/repower?Format=XML'


class RepowerService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_repower(self, repower_request):
        body = self.generate_xml(repower_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_xml(self, repower_request):
        el_repower_request = ET.Element('RepowerRequest')
        el_transaction_reference = ET.SubElement(el_repower_request, 'TransactionReference')
        el_transaction_reference.text = repower_request.transaction_reference
        el_card_number = ET.SubElement(el_repower_request, 'CardNumber')
        el_card_number.text = repower_request.card_number
        el_transaction_amount = ET.SubElement(el_repower_request, 'TransactionAmount')
        el_value = ET.SubElement(el_transaction_amount, 'Value')
        el_value.text = repower_request.transaction_amount.value
        el_currency = ET.SubElement(el_transaction_amount, 'Currency')
        el_currency.text = repower_request.transaction_amount.currency
        el_local_date = ET.SubElement(el_repower_request, 'LocalDate')
        el_local_date.text = repower_request.local_date
        el_local_time = ET.SubElement(el_repower_request, 'LocalTime')
        el_local_time.text = repower_request.local_time
        el_channel = ET.SubElement(el_repower_request, 'Channel')
        el_channel.text = repower_request.channel
        el_ica = ET.SubElement(el_repower_request, 'ICA')
        el_ica.text = repower_request.ica
        el_processor_id = ET.SubElement(el_repower_request, 'ProcessorId')
        el_processor_id.text = repower_request.processor_id
        el_routing_and_transit_number = ET.SubElement(el_repower_request, 'RoutingAndTransitNumber')
        el_routing_and_transit_number.text = repower_request.routing_and_transit_number
        el_merchant_type = ET.SubElement(el_repower_request, 'MerchantType')
        el_merchant_type.text = repower_request.merchant_type
        el_card_acceptor = ET.SubElement(el_repower_request, 'CardAcceptor')
        el_card_acceptor_name = ET.SubElement(el_card_acceptor, 'Name')
        el_card_acceptor_name.text = repower_request.card_acceptor.name
        el_card_acceptor_city = ET.SubElement(el_card_acceptor, 'City')
        el_card_acceptor_city.text = repower_request.card_acceptor.city
        el_card_acceptor_state = ET.SubElement(el_card_acceptor, 'State')
        el_card_acceptor_state.text = repower_request.card_acceptor.state
        el_card_acceptor_postal_code = ET.SubElement(el_card_acceptor, 'PostalCode')
        el_card_acceptor_postal_code.text = repower_request.card_acceptor.postal_code
        el_card_acceptor_country = ET.SubElement(el_card_acceptor, 'Country')
        el_card_acceptor_country.text = repower_request.card_acceptor.country
        return ET.tostring(el_repower_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        re_power = repower.Repower()
        re_power.request_id = none_check.verify_not_none(xml_response.find('RequestId'))
        re_power.transaction_reference = none_check.verify_not_none(xml_response.find('TransactionReference'))

        transaction_history = transactionhistory.TransactionHistory()
        xml_transaction_history = xml_response.find('TransactionHistory')

        transaction_ = transaction.Transaction()
        xml_transaction = xml_transaction_history.find('Transaction')
        transaction_.type = none_check.verify_not_none(xml_transaction.find('Type'))
        transaction_.system_trace_audit_number = none_check.verify_not_none(xml_transaction.find('SystemTraceAuditNumber'))
        transaction_.network_reference_number = none_check.verify_not_none(xml_transaction.find('NetworkReferenceNumber'))
        transaction_.settlement_date = none_check.verify_not_none(xml_transaction.find('SettlementDate'))

        response_ = response.Response()
        xml_response = xml_transaction.find('Response')
        response_.code = none_check.verify_not_none(xml_response.find('Code'))
        response_.description = none_check.verify_not_none(xml_response.find('Description'))

        transaction_.submit_date_time = none_check.verify_not_none(xml_transaction.find('SubmitDateTime'))

        transaction_.response = response_
        transaction_history.transaction = transaction_

        account_balance = accountbalance.AccountBalance()
        account_balance.value = none_check.verify_not_none(xml_response.find('AccountBalance/Value'))
        account_balance.currency = none_check.verify_not_none(xml_response.find('AccountBalance/Currency'))

        re_power.transaction_history = transaction_history
        re_power.account_balance = account_balance
        return re_power
