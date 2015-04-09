from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.moneysend.domain.transfer import transferreversal
from services.moneysend.domain.transfer import transferreversalrequest
from services.moneysend.domain.transfer import transactionhistory
from services.moneysend.domain.transfer import transaction
from services.moneysend.domain.transfer import response

PRODUCTION_URL = 'https://api.mastercard.com/moneysend/v2/transferreversal?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/moneysend/v2/transferreversal?Format=XML'


class TransferReversalService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_transfer_reversal(self, request):
        body = self.generate_xml(request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_xml(self, transfer_request):
        el_transfer_reversal_request = ET.Element('TransferReversalRequest')
        el_ica = ET.SubElement(el_transfer_reversal_request, 'ICA')
        el_ica.text = transfer_request.ica
        el_transaction_reference = ET.SubElement(el_transfer_reversal_request, 'TransactionReference')
        el_transaction_reference.text = transfer_request.transaction_reference
        el_reversal_reason = ET.SubElement(el_transfer_reversal_request, 'ReversalReason')
        el_reversal_reason.text = transfer_request.reversal_reason
        return ET.tostring(el_transfer_reversal_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        transfer_reversal = transferreversal.TransferReversal()
        transfer_reversal.request_id = none_check.verify_not_none(xml_response.find('RequestId'))
        transfer_reversal.original_request_id = none_check.verify_not_none(xml_response.find('OriginalRequestId'))
        transfer_reversal.transaction_reference = none_check.verify_not_none(xml_response.find('TransactionReference'))

        transaction_history = transactionhistory.TransactionHistory()
        transaction_ = transaction.Transaction()
        xml_transaction = xml_response.find('TransactionHistory/Transaction')
        transaction_.type = none_check.verify_not_none(xml_transaction.find('Type'))
        transaction_.system_trace_audit_number = none_check.verify_not_none(xml_transaction.find('SystemTraceAuditNumber'))
        transaction_.network_reference_number = none_check.verify_not_none(xml_transaction.find('NetworkReferenceNumber'))
        transaction_.settlement_date = none_check.verify_not_none(xml_transaction.find('SettlementDate'))

        response_ = response.Response()
        response_.code = none_check.verify_not_none(xml_transaction.find('Response/Code'))
        response_.description = none_check.verify_not_none(xml_transaction.find('Response/Description'))
        transaction_.response = response_

        transaction_.submit_date_time = none_check.verify_not_none(xml_transaction.find('SubmitDateTime'))
        transaction_history.transaction = transaction_
        transfer_reversal.transaction_history = transaction_history
        return transfer_reversal