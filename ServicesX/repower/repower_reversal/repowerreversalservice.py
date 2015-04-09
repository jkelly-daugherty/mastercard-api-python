from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.repower.repower_reversal.domain import repowerreversal
from services.repower.repower_reversal.domain import repowerreversalrequest
from services.repower.repower.domain import transactionhistory
from services.repower.repower.domain import transaction
from services.repower.repower.domain import response

PRODUCTION_URL = 'https://api.mastercard.com/repower/v1/repowerreversal?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/repower/v1/repowerreversal?Format=XML'


class RepowerReversalService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_repower_reversal(self, repower_reversal):
        body = self.generate_xml(repower_reversal)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_xml(self, repower_request):
        el_repower_reversal_request = ET.Element('RepowerReversalRequest')
        el_ica = ET.SubElement(el_repower_reversal_request, 'ICA')
        el_ica.text = repower_request.ica
        el_transaction_reference = ET.SubElement(el_repower_reversal_request, 'TransactionReference')
        el_transaction_reference.text = repower_request.transaction_reference
        el_reversal_reason = ET.SubElement(el_repower_reversal_request, 'ReversalReason')
        el_reversal_reason.text = repower_request.reversal_reason
        return ET.tostring(el_repower_reversal_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        re_power_reversal = repowerreversal.RepowerReversal()
        re_power_reversal.request_id = none_check.verify_not_none(xml_response.find('RequestId'))
        re_power_reversal.original_request_id = none_check.verify_not_none(xml_response.find('OriginalRequestId'))
        re_power_reversal.transaction_reference = none_check.verify_not_none(xml_response.find('TransactionReference'))

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

        re_power_reversal.transaction_history = transaction_history
        return re_power_reversal
