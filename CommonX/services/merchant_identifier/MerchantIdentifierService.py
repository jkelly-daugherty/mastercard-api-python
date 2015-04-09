from common import connector
from common import urlutil
from common import environment
import xml.etree.ElementTree as ET
from services.merchant_identifier.domain import merchantids
from services.merchant_identifier.domain import address
from services.merchant_identifier.domain import merchant
from services.merchant_identifier.domain import returnedmerchants
from services.merchant_identifier.domain import country
from services.merchant_identifier.domain import countrysubdivision

PRODUCTION_URL = 'https://api.mastercard.com/merchantid/v1/merchantid?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/merchantid/v1/merchantid?Format=XML'


class MerchantIdentifierService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_merchant_ids(self, options):
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self, options):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL

        url = urlutil.UrlUtil.add_query_parameter(url, "MerchantId", options.merchant_id)
        url = urlutil.UrlUtil.add_query_parameter(url, "Type", options.type)
        return url

    def generate_return_object(self, xml_response):
        message = xml_response.find('Message').text
        merchant_array = list()
        for xml_merchant in xml_response.findall('.//Merchant'):
            tmp_address = address.Address()
            tmp_address.line1 = xml_merchant.find('Address/Line1').text
            tmp_address.line2 = xml_merchant.find('Address/Line2').text
            tmp_address.city = xml_merchant.find('Address/City').text
            tmp_address.postal_code = xml_merchant.find('Address/PostalCode').text

            tmp_country_subdivision = countrysubdivision.CountrySubdivision()
            tmp_country_subdivision.name = xml_merchant.find('Address/CountrySubdivision/Name').text
            tmp_country_subdivision.code = xml_merchant.find('Address/CountrySubdivision/Code').text
            tmp_address.country_subdivision = tmp_country_subdivision

            tmp_country = country.Country()
            tmp_country.name = xml_merchant.find('Address/Country/Name').text
            tmp_country.code = xml_merchant.find('Address/Country/Code').text
            tmp_address.country = tmp_country

            tmp_merchant = merchant.Merchant()
            tmp_merchant.address = tmp_address
            tmp_merchant.phone_number = xml_merchant.find('PhoneNumber').text
            tmp_merchant.brand_name = xml_merchant.find('BrandName').text
            tmp_merchant.merchant_category = xml_merchant.find('MerchantCategory').text
            tmp_merchant.merchant_dba_name = xml_merchant.find('MerchantDbaName').text
            tmp_merchant.descriptor_text = xml_merchant.find('DescriptorText').text
            tmp_merchant.legal_corporate_name = xml_merchant.find('LegalCorporateName').text
            tmp_merchant.brick_count = xml_merchant.find('BrickCount').text
            tmp_merchant.comment = xml_merchant.find('Comment').text
            tmp_merchant.location_id = xml_merchant.find('LocationId').text
            tmp_merchant.online_count = xml_merchant.find('OnlineCount').text
            tmp_merchant.other_count = xml_merchant.find('OtherCount').text
            tmp_merchant.sole_proprietor_name = xml_merchant.find('SoleProprietorName').text

            merchant_array.append(tmp_merchant)
        returned_merchants = returnedmerchants.ReturnedMerchants(merchant_array)
        merchant_ids = merchantids.MerchantIds(message, returned_merchants)
        return merchant_ids