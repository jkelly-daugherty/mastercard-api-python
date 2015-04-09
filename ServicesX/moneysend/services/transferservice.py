from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.moneysend.domain.transfer import transfer
from services.moneysend.domain.transfer import transferrequest
from services.moneysend.domain.transfer import paymentrequest
from services.moneysend.domain.transfer import transactionhistory
from services.moneysend.domain.transfer import transaction
from services.moneysend.domain.transfer import response

PRODUCTION_URL = 'https://api.mastercard.com/moneysend/v2/transfer?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/moneysend/v2/transfer?Format=XML'


class TransferService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_transfer(self, request):
        body = ''
        if isinstance(request, transferrequest.TransferRequest):
            body = self.generate_transfer_xml(request)
        elif isinstance(request, paymentrequest.PaymentRequest):
            body = self.generate_payment_xml(request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_transfer_xml(self, transfer_request):
        el_transfer_request = ET.Element('TransferRequest')
        el_local_date = ET.SubElement(el_transfer_request, 'LocalDate')
        el_local_date.text = transfer_request.local_date
        el_local_time = ET.SubElement(el_transfer_request, 'LocalTime')
        el_local_time.text = transfer_request.local_time
        el_transaction_reference = ET.SubElement(el_transfer_request, 'TransactionReference')
        el_transaction_reference.text = transfer_request.transaction_reference
        if transfer_request.sender_name != '':
            el_sender_name = ET.SubElement(el_transfer_request, 'SenderName')
            el_sender_name.text = transfer_request.sender_name
            el_sender_address = ET.SubElement(el_transfer_request, 'SenderAddress')
            el_sender_line1 = ET.SubElement(el_sender_address, 'Line1')
            el_sender_line1.text = transfer_request.sender_address.line1
            el_sender_line2 = ET.SubElement(el_sender_address, 'Line2')
            el_sender_line2.text = transfer_request.sender_address.line2
            el_sender_city = ET.SubElement(el_sender_address, 'City')
            el_sender_city.text = transfer_request.sender_address.city
            el_sender_country_subdivision = ET.SubElement(el_sender_address, 'CountrySubdivision')
            el_sender_country_subdivision.text = transfer_request.sender_address.country_subdivision
            el_sender_postal_code = ET.SubElement(el_sender_address, 'PostalCode')
            el_sender_postal_code.text = transfer_request.sender_address.postal_code
            el_sender_country = ET.SubElement(el_sender_address, 'Country')
            el_sender_country.text = transfer_request.sender_address.country
            el_funding_card = ET.SubElement(el_transfer_request, 'FundingCard')
            el_funding_account_number = ET.SubElement(el_funding_card, 'AccountNumber')
            el_funding_account_number.text = transfer_request.funding_card.account_number
            el_funding_expiry_month = ET.SubElement(el_funding_card, 'ExpiryMonth')
            el_funding_expiry_month.text = transfer_request.funding_card.expiry_month
            el_funding_expiry_year = ET.SubElement(el_funding_card, 'ExpiryYear')
            el_funding_expiry_year.text = transfer_request.funding_card.expiry_year
        else:
            el_funding_mapped = ET.SubElement(el_transfer_request, 'FundingMapped')
            el_subscriber_id = ET.SubElement(el_funding_mapped, 'SubscriberId')
            el_subscriber_id.text = transfer_request.funding_mapped.subscriber_id
            el_subscriber_type = ET.SubElement(el_funding_mapped, 'SubscriberType')
            el_subscriber_type.text = transfer_request.funding_mapped.subscriber_type
            el_subscriber_alias = ET.SubElement(el_funding_mapped, 'SubscriberAlias')
            el_subscriber_alias.text = transfer_request.funding_mapped.subscriber_alias
        el_funding_ucaf = ET.SubElement(el_transfer_request, 'FundingUCAF')
        el_funding_ucaf.text = transfer_request.funding_ucaf
        el_funding_mastercard_assigned_id = ET.SubElement(el_transfer_request, 'FundingMasterCardAssignedId')
        el_funding_mastercard_assigned_id.text = transfer_request.funding_mastercard_assigned_id
        el_funding_amount = ET.SubElement(el_transfer_request, 'FundingAmount')
        el_funding_value = ET.SubElement(el_funding_amount, 'Value')
        el_funding_value.text = transfer_request.funding_amount.value
        el_funding_currency = ET.SubElement(el_funding_amount, 'Currency')
        el_funding_currency.text = transfer_request.funding_amount.currency
        el_receiver_name = ET.SubElement(el_transfer_request, 'ReceiverName')
        el_receiver_name.text = transfer_request.receiver_name
        el_receiver_address = ET.SubElement(el_transfer_request, 'ReceiverAddress')
        el_receiver_line1 = ET.SubElement(el_receiver_address, 'Line1')
        el_receiver_line1.text = transfer_request.receiver_address.line1
        el_receiver_line2 = ET.SubElement(el_receiver_address, 'Line2')
        el_receiver_line2.text = transfer_request.receiver_address.line2
        el_receiver_city = ET.SubElement(el_receiver_address, 'City')
        el_receiver_city.text = transfer_request.receiver_address.city
        el_receiver_country_subdivision = ET.SubElement(el_receiver_address, 'CountrySubdivision')
        el_receiver_country_subdivision.text = transfer_request.receiver_address.country_subdivision
        el_receiver_postal_code = ET.SubElement(el_receiver_address, 'PostalCode')
        el_receiver_postal_code.text = transfer_request.receiver_address.postal_code
        el_receiver_country = ET.SubElement(el_receiver_address, 'Country')
        el_receiver_country.text = transfer_request.receiver_address.country
        el_receiver_phone = ET.SubElement(el_transfer_request, 'ReceiverPhone')
        el_receiver_phone.text = transfer_request.receiver_phone
        el_receiving_card = ET.SubElement(el_transfer_request, 'ReceivingCard')
        el_receiving_account_number = ET.SubElement(el_receiving_card, 'AccountNumber')
        el_receiving_account_number.text = transfer_request.receiving_card.account_number
        el_receiving_amount = ET.SubElement(el_transfer_request, 'ReceivingAmount')
        el_receiving_value = ET.SubElement(el_receiving_amount, 'Value')
        el_receiving_value.text = transfer_request.receiving_amount.value
        el_receiving_currency = ET.SubElement(el_receiving_amount, 'Currency')
        el_receiving_currency.text = transfer_request.receiving_amount.currency
        el_channel = ET.SubElement(el_transfer_request, 'Channel')
        el_channel.text = transfer_request.channel
        el_ucaf_support = ET.SubElement(el_transfer_request, 'UCAFSupport')
        el_ucaf_support.text = transfer_request.ucaf_support
        el_ica = ET.SubElement(el_transfer_request, 'ICA')
        el_ica.text = transfer_request.ica
        el_processor_id = ET.SubElement(el_transfer_request, 'ProcessorId')
        el_processor_id.text = transfer_request.processor_id
        el_routing_and_transit_number = ET.SubElement(el_transfer_request, 'RoutingAndTransitNumber')
        el_routing_and_transit_number.text = transfer_request.routing_and_transit_number
        el_card_acceptor = ET.SubElement(el_transfer_request, 'CardAcceptor')
        el_acceptor_name = ET.SubElement(el_card_acceptor, 'Name')
        el_acceptor_name.text = transfer_request.card_acceptor.name
        el_acceptor_city = ET.SubElement(el_card_acceptor, 'City')
        el_acceptor_city.text = transfer_request.card_acceptor.city
        el_acceptor_state = ET.SubElement(el_card_acceptor, 'State')
        el_acceptor_state.text = transfer_request.card_acceptor.state
        el_acceptor_postal_code = ET.SubElement(el_card_acceptor, 'PostalCode')
        el_acceptor_postal_code.text = transfer_request.card_acceptor.postal_code
        el_acceptor_country = ET.SubElement(el_card_acceptor, 'Country')
        el_acceptor_country.text = transfer_request.card_acceptor.country
        el_transaction_desc = ET.SubElement(el_transfer_request, 'TransactionDesc')
        el_transaction_desc.text = transfer_request.transaction_desc
        el_merchant_id = ET.SubElement(el_transfer_request, 'MerchantId')
        el_merchant_id.text = transfer_request.merchant_id
        return ET.tostring(el_transfer_request, encoding="unicode")

    def generate_payment_xml(self, payment_request):
        el_payment_request = ET.Element('PaymentRequest')
        el_local_date = ET.SubElement(el_payment_request, 'LocalDate')
        el_local_date.text = payment_request.local_date
        el_local_time = ET.SubElement(el_payment_request, 'LocalTime')
        el_local_time.text = payment_request.local_time
        el_transaction_reference = ET.SubElement(el_payment_request, 'TransactionReference')
        el_transaction_reference.text = payment_request.transaction_reference
        el_sender_name = ET.SubElement(el_payment_request, 'SenderName')
        el_sender_name.text = payment_request.sender_name
        el_sender_address = ET.SubElement(el_payment_request, 'SenderAddress')
        el_sender_line1 = ET.SubElement(el_sender_address, 'Line1')
        el_sender_line1.text = payment_request.sender_address.line1
        el_sender_line2 = ET.SubElement(el_sender_address, 'Line2')
        el_sender_line2.text = payment_request.sender_address.line2
        el_sender_city = ET.SubElement(el_sender_address, 'City')
        el_sender_city.text = payment_request.sender_address.city
        el_sender_country_subdivision = ET.SubElement(el_sender_address, 'CountrySubdivision')
        el_sender_country_subdivision.text = payment_request.sender_address.country_subdivision
        el_sender_postal_code = ET.SubElement(el_sender_address, 'PostalCode')
        el_sender_postal_code.text = payment_request.sender_address.postal_code
        el_sender_country = ET.SubElement(el_sender_address, 'Country')
        el_sender_country.text = payment_request.sender_address.country
        if payment_request.receiving_card != '':
            el_receiving_card = ET.SubElement(el_payment_request, 'ReceivingCard')
            el_receiving_account_number = ET.SubElement(el_receiving_card, 'AccountNumber')
            el_receiving_account_number.text = payment_request.receiving_card.account_number
        else:
            el_receiving_mapped = ET.SubElement(el_payment_request, 'ReceivingMapped')
            el_subscriber_id = ET.SubElement(el_receiving_mapped, 'SubscriberId')
            el_subscriber_id.text = payment_request.receiving_mapped.subscriber_id
            el_subscriber_type = ET.SubElement(el_receiving_mapped, 'SubscriberType')
            el_subscriber_type.text = payment_request.receiving_mapped.subscriber_type
            el_subscriber_alias = ET.SubElement(el_receiving_mapped, 'SubscriberAlias')
            el_subscriber_alias.text = payment_request.receiving_mapped.subscriber_alias
        el_receiving_amount = ET.SubElement(el_payment_request, 'ReceivingAmount')
        el_receiving_value = ET.SubElement(el_receiving_amount, 'Value')
        el_receiving_value.text = payment_request.receiving_amount.value
        el_receiving_currency = ET.SubElement(el_receiving_amount, 'Currency')
        el_receiving_currency.text = payment_request.receiving_amount.currency
        el_ica = ET.SubElement(el_payment_request, 'ICA')
        el_ica.text = payment_request.ica
        el_processor_id = ET.SubElement(el_payment_request, 'ProcessorId')
        el_processor_id.text = payment_request.processor_id
        el_routing_and_transit_number = ET.SubElement(el_payment_request, 'RoutingAndTransitNumber')
        el_routing_and_transit_number.text = payment_request.routing_and_transit_number
        el_card_acceptor = ET.SubElement(el_payment_request, 'CardAcceptor')
        el_acceptor_name = ET.SubElement(el_card_acceptor, 'Name')
        el_acceptor_name.text = payment_request.card_acceptor.name
        el_acceptor_city = ET.SubElement(el_card_acceptor, 'City')
        el_acceptor_city.text = payment_request.card_acceptor.city
        el_acceptor_state = ET.SubElement(el_card_acceptor, 'State')
        el_acceptor_state.text = payment_request.card_acceptor.state
        el_acceptor_postal_code = ET.SubElement(el_card_acceptor, 'PostalCode')
        el_acceptor_postal_code.text = payment_request.card_acceptor.postal_code
        el_acceptor_country = ET.SubElement(el_card_acceptor, 'Country')
        el_acceptor_country.text = payment_request.card_acceptor.country
        el_transaction_desc = ET.SubElement(el_payment_request, 'TransactionDesc')
        el_transaction_desc.text = payment_request.transaction_desc
        el_merchant_id = ET.SubElement(el_payment_request, 'MerchantId')
        el_merchant_id.text = payment_request.merchant_id
        return ET.tostring(el_payment_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        transfer_ = transfer.Transfer()
        transfer_.request_id = none_check.verify_not_none(xml_response.find('RequestId'))
        transfer_.transaction_reference = none_check.verify_not_none(xml_response.find('TransactionReference'))

        transaction_history = transactionhistory.TransactionHistory()
        transaction_list = list()

        for xml_transaction in xml_response.findall('.//Transaction'):
            transaction_ = transaction.Transaction()
            transaction_.type = none_check.verify_not_none(xml_transaction.find('Type'))
            transaction_.system_trace_audit_number = none_check.verify_not_none(xml_transaction.find('SystemTraceAuditNumber'))
            transaction_.network_reference_number = none_check.verify_not_none(xml_transaction.find('NetworkReferenceNumber'))
            transaction_.settlement_date = none_check.verify_not_none(xml_transaction.find('SettlementDate'))

            response_ = response.Response()
            response_.code = none_check.verify_not_none(xml_transaction.find('Response/Code'))
            response_.description = none_check.verify_not_none(xml_transaction.find('Response/Description'))
            transaction_.response = response_

            transaction_.submit_date_time = none_check.verify_not_none(xml_transaction.find('SubmitDateTime'))
            transaction_list.append(transaction_)
        transaction_history.transaction = transaction_list
        transfer_.transaction_history = transaction_history
        return transfer_