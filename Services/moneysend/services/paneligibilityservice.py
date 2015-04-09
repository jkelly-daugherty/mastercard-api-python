from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.moneysend.domain.pan_eligibility import paneligibility
from services.moneysend.domain.pan_eligibility import paneligibilityrequest
from services.moneysend.domain.common import receivingeligibility
from services.moneysend.domain.common import sendingeligibility
from services.moneysend.domain.common import country
from services.moneysend.domain.common import currency
from services.moneysend.domain.common import brand

PRODUCTION_URL = 'https://api.mastercard.com/moneysend/v2/eligibility/pan?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/moneysend/v2/eligibility/pan?Format=XML'


class PanEligibilityService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_pan_eligibility(self, pan_eligibility_request):
        body = self.generate_xml(pan_eligibility_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def get_url(self, options=None):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_xml(self, pan_eligibility_request):
        el_pan_eligibility_request = ET.Element('PanEligibilityRequest')
        if pan_eligibility_request.sending_account_number is not None \
                and pan_eligibility_request.sending_account_number != '':
            el_sending_account_number = ET.SubElement(el_pan_eligibility_request, 'SendingAccountNumber')
            el_sending_account_number.text = pan_eligibility_request.sending_account_number
        if pan_eligibility_request.receiving_account_number is not None \
                and pan_eligibility_request.receiving_account_number != '':
            el_receiving_account_number = ET.SubElement(el_pan_eligibility_request, 'ReceivingAccountNumber')
            el_receiving_account_number.text = pan_eligibility_request.receiving_account_number
        return ET.tostring(el_pan_eligibility_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        pan_eligibility = paneligibility.PanEligibility()
        pan_eligibility.request_id = none_check.verify_not_none(xml_response.find('RequestId'))
        if xml_response.find('SendingEligibility') is not None:
            tmp_sending_eligibility = sendingeligibility.SendingEligibility()
            xml_sending_eligibility = xml_response.find('SendingEligibility')
            tmp_sending_eligibility.eligible = none_check.verify_not_none(xml_sending_eligibility.find('Eligible'))
            tmp_sending_eligibility.reason_code = none_check.verify_not_none(xml_sending_eligibility.find('ReasonCode'))
            tmp_sending_eligibility.account_number = none_check.verify_not_none(xml_sending_eligibility.find('AccountNumber'))
            tmp_sending_eligibility.ica = none_check.verify_not_none(xml_sending_eligibility.find('ICA'))

            if xml_sending_eligibility.find('Currency') is not None:
                tmp_currency = currency.Currency()
                xml_currency = xml_sending_eligibility.find('Currency')
                tmp_currency.alpha_currency_code = none_check.verify_not_none(xml_currency.find('AlphaCurrencyCode'))
                tmp_currency.numeric_currency_code = none_check.verify_not_none(xml_currency.find('NumericCurrencyCode'))
                tmp_sending_eligibility.currency = tmp_currency

            if xml_sending_eligibility.find('Country') is not None:
                tmp_country = country.Country()
                xml_country = xml_sending_eligibility.find('Country')
                tmp_country.alpha_country_code = none_check.verify_not_none(xml_country.find('AlphaCountryCode'))
                tmp_country.numeric_country_code = none_check.verify_not_none(xml_country.find('NumericCountryCode'))
                tmp_sending_eligibility.country = tmp_country

            if xml_sending_eligibility.find('Brand') is not None:
                tmp_brand = brand.Brand()
                xml_brand = xml_sending_eligibility.find('Brand')
                tmp_brand.acceptance_brand_code_code = none_check.verify_not_none(xml_brand.find('AcceptanceBrandCode'))
                tmp_brand.numeric_country_code = none_check.verify_not_none(xml_brand.find('ProductBrandCode'))
                tmp_sending_eligibility.brand = tmp_brand

            pan_eligibility.sending_eligibility = tmp_sending_eligibility

        if xml_response.find('ReceivingEligibility') is not None:
            tmp_receiving_eligibility = receivingeligibility.ReceivingEligibility()
            xml_receiving_eligibility = xml_response.find('ReceivingEligibility')
            tmp_receiving_eligibility.eligible = none_check.verify_not_none(xml_receiving_eligibility.find('Eligible'))
            tmp_receiving_eligibility.reason_code = none_check.verify_not_none(xml_receiving_eligibility.find('ReasonCode'))
            tmp_receiving_eligibility.account_number = none_check.verify_not_none(xml_receiving_eligibility.find('AccountNumber'))
            tmp_receiving_eligibility.ica = none_check.verify_not_none(xml_receiving_eligibility.find('ICA'))

            if xml_receiving_eligibility.find('Currency') is not None:
                tmp_currency = currency.Currency()
                xml_currency = xml_receiving_eligibility.find('Currency')
                tmp_currency.alpha_currency_code = none_check.verify_not_none(xml_currency.find('AlphaCurrencyCode'))
                tmp_currency.numeric_currency_code = none_check.verify_not_none(xml_currency.find('NumericCurrencyCode'))
                tmp_receiving_eligibility.currency = tmp_currency

            if xml_receiving_eligibility.find('Country') is not None:
                tmp_country = country.Country()
                xml_country = xml_receiving_eligibility.find('Country')
                tmp_country.alpha_country_code = none_check.verify_not_none(xml_country.find('AlphaCountryCode'))
                tmp_country.numeric_country_code = none_check.verify_not_none(xml_country.find('NumericCountryCode'))
                tmp_receiving_eligibility.country = tmp_country

            if xml_receiving_eligibility.find('Brand') is not None:
                tmp_brand = brand.Brand()
                xml_brand = xml_receiving_eligibility.find('Brand')
                tmp_brand.acceptance_brand_code_code = none_check.verify_not_none(xml_brand.find('AcceptanceBrandCode'))
                tmp_brand.numeric_country_code = none_check.verify_not_none(xml_brand.find('ProductBrandCode'))
                tmp_receiving_eligibility.brand = tmp_brand

            pan_eligibility.receiving_eligibility = tmp_receiving_eligibility

        return pan_eligibility