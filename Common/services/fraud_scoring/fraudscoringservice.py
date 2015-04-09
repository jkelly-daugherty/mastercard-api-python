from common import connector
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.fraud_scoring.domain import scorelookup
from services.fraud_scoring.domain import scoreresponse
from services.fraud_scoring.domain import transactiondetail

PRODUCTION_URL = 'https://api.mastercard.com/fraud/merchantscoring/v1/score-lookup?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/fraud/merchantscoring/v1/score-lookup?Format=XML'


class FraudScoringService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_score_lookup(self, lookup_request):
        body = self.generate_xml(lookup_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def generate_xml(self, lookup_request):
        el_score_lookup_request = ET.Element('ScoreLookupRequest')
        el_transaction_detail = ET.SubElement(el_score_lookup_request, 'TransactionDetail')
        el_customer_identifier = ET.SubElement(el_transaction_detail, "CustomerIdentifier")
        el_customer_identifier.text = lookup_request.transaction_detail.customer_identifier
        el_merchant_identifier = ET.SubElement(el_transaction_detail, "MerchantIdentifier")
        el_merchant_identifier.text = lookup_request.transaction_detail.merchant_identifier
        el_account_number = ET.SubElement(el_transaction_detail, "AccountNumber")
        el_account_number.text = lookup_request.transaction_detail.account_number
        el_account_prefix = ET.SubElement(el_transaction_detail, "AccountPrefix")
        el_account_prefix.text = lookup_request.transaction_detail.account_prefix
        el_account_suffix = ET.SubElement(el_transaction_detail, "AccountSuffix")
        el_account_suffix.text = lookup_request.transaction_detail.account_suffix
        el_transaction_amount = ET.SubElement(el_transaction_detail, "TransactionAmount")
        el_transaction_amount.text = lookup_request.transaction_detail.transaction_amount
        el_transaction_date = ET.SubElement(el_transaction_detail, "TransactionDate")
        el_transaction_date.text = lookup_request.transaction_detail.transaction_date
        el_transaction_time = ET.SubElement(el_transaction_detail, "TransactionTime")
        el_transaction_time.text = lookup_request.transaction_detail.transaction_time
        el_bank_net_reference_number = ET.SubElement(el_transaction_detail, "BankNetReferenceNumber")
        el_bank_net_reference_number.text = lookup_request.transaction_detail.bank_net_reference_number
        el_stan = ET.SubElement(el_transaction_detail, "Stan")
        el_stan.text = lookup_request.transaction_detail.stan
        return ET.tostring(el_score_lookup_request, encoding="unicode")

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()

        score_lookup = scorelookup.ScoreLookup()
        score_lookup.customer_identifier = none_check.verify_not_none(xml_response.find('CustomerIdentifier'))
        score_lookup.request_timestamp = none_check.verify_not_none(xml_response.find('RequestTimestamp'))

        xml_transaction_detail = xml_response.find('TransactionDetail')
        transaction_detail = transactiondetail.TransactionDetail()
        transaction_detail.customer_identifier = none_check.verify_not_none(xml_transaction_detail.find('CustomerIdentifier'))
        transaction_detail.merchant_identifier = none_check.verify_not_none(xml_transaction_detail.find('MerchantIdentifier'))
        transaction_detail.account_number = none_check.verify_not_none(xml_transaction_detail.find('AccountNumber'))
        transaction_detail.account_prefix = none_check.verify_not_none(xml_transaction_detail.find('AccountPrefix'))
        transaction_detail.account_suffix = none_check.verify_not_none(xml_transaction_detail.find('AccountSuffix'))
        transaction_detail.transaction_amount = none_check.verify_not_none(xml_transaction_detail.find('TransactionAmount'))
        transaction_detail.transaction_date = none_check.verify_not_none(xml_transaction_detail.find('TransactionDate'))
        transaction_detail.transaction_time = none_check.verify_not_none(xml_transaction_detail.find('TransactionTime'))
        transaction_detail.bank_net_reference_number = none_check.verify_not_none(xml_transaction_detail.find('BankNetReferenceNumber'))
        transaction_detail.stan = none_check.verify_not_none(xml_transaction_detail.find('Stan'))

        xml_score_response = xml_response.find('ScoreResponse')
        score_response = scoreresponse.ScoreResponse()
        score_response.match_indicator = none_check.verify_not_none(xml_score_response.find('MatchIndicator'))
        # If statement used for NO_MATCH_FOUND response. MatchIndicator will equal 4 and other values will be none
        if xml_score_response.find('FraudScore') is not None:
            score_response.fraud_score = none_check.verify_not_none(xml_score_response.find('FraudScore'))
            score_response.reason_code = none_check.verify_not_none(xml_score_response.find('ReasonCode'))
            score_response.rules_adjusted_score = none_check.verify_not_none(xml_score_response.find('RulesAdjustedScore'))
            score_response.rules_adjusted_reason_code = none_check.verify_not_none(xml_score_response.find('RulesAdjustedReasonCode'))
            score_response.rules_adjusted_reason_code_secondary = none_check.verify_not_none(xml_score_response.find('RulesAdjustedReasonCodeSecondary'))
        score_lookup.transaction_detail = transaction_detail
        score_lookup.score_response = score_response
        return score_lookup