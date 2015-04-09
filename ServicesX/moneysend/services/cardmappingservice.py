from common import connector
from common import urlutil
from common import environment
import xml.etree.ElementTree as ET
from services.moneysend.domain.card_mapping import createmapping
from services.moneysend.domain.card_mapping import createmappingrequest
from services.moneysend.domain.card_mapping import inquiremapping
from services.moneysend.domain.card_mapping import inquiremappingrequest
from services.moneysend.domain.card_mapping import updatemapping
from services.moneysend.domain.card_mapping import updatemappingrequest
from services.moneysend.domain.card_mapping import deletemapping
from services.moneysend.domain.common import address
from services.moneysend.domain.common import mapping
from services.moneysend.domain.common import mappings
from services.moneysend.domain.common import cardholderfullname
from services.moneysend.domain.common import receivingeligibility
from services.moneysend.domain.common import currency
from services.moneysend.domain.common import country
from services.moneysend.domain.common import brand

PRODUCTION_URL = 'https://api.mastercard.com/moneysend/v2/mapping/card?Format=XML'
SANDBOX_URL = 'https://sandbox.api.mastercard.com/moneysend/v2/mapping/card?Format=XML'


class CardMappingService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_create_mapping(self, create_mapping_request):
        body = self.generate_xml(create_mapping_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_inquire_mapping(self, inquire_mapping_request):
        body = self.generate_xml(inquire_mapping_request)
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def get_update_mapping(self, update_mapping_request, options):
        body = self.generate_xml(update_mapping_request)
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'PUT', body))
        return self.generate_return_object(xml_response)

    def get_delete_mapping(self, options):
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'DELETE'))
        return self.generate_return_object(xml_response)

    def get_url(self, options=None):
        url = 'https://sandbox.api.mastercard.com/moneysend/v2/mapping/card/{mapping_id}?Format=XML'
        if self.environment == environment.Environment.PRODUCTION:
            url = 'https://api.mastercard.com/moneysend/v2/mapping/card/{mapping_id}?Format=XML'

        if options is not None:
            url = url.replace("{mapping_id}", options.mapping_id)
        else:
            url = url.replace("{mapping_id}", "")
        return url

    def generate_xml(self, mapping_request):
        if isinstance(mapping_request, createmappingrequest.CreateMappingRequest):
            el_create_mapping_request = ET.Element('CreateMappingRequest')
            el_subscriber_id = ET.SubElement(el_create_mapping_request, 'SubscriberId')
            el_subscriber_id.text = mapping_request.subscriber_id
            el_subscriber_type = ET.SubElement(el_create_mapping_request, 'SubscriberType')
            el_subscriber_type.text = mapping_request.subscriber_type
            el_account_usage = ET.SubElement(el_create_mapping_request, 'AccountUsage')
            el_account_usage.text = mapping_request.account_usage
            el_default_indicator = ET.SubElement(el_create_mapping_request, 'DefaultIndicator')
            el_default_indicator.text = mapping_request.default_indicator
            el_alias = ET.SubElement(el_create_mapping_request, 'Alias')
            el_alias.text = mapping_request.alias
            el_ica = ET.SubElement(el_create_mapping_request, 'ICA')
            el_ica.text = mapping_request.ica
            el_account_number = ET.SubElement(el_create_mapping_request, 'AccountNumber')
            el_account_number.text = mapping_request.account_number
            el_expiry_date = ET.SubElement(el_create_mapping_request, 'ExpiryDate')
            el_expiry_date.text = mapping_request.expiry_date
            el_cardholder_full_name = ET.SubElement(el_create_mapping_request, 'CardholderFullName')
            el_cardholder_first_name = ET.SubElement(el_cardholder_full_name, 'CardholderFirstName')
            el_cardholder_first_name.text = mapping_request.cardholder_full_name.cardholder_first_name
            el_cardholder_middle_name = ET.SubElement(el_cardholder_full_name, 'CardholderMiddleName')
            el_cardholder_middle_name.text = mapping_request.cardholder_full_name.cardholder_middle_name
            el_cardholder_last_name = ET.SubElement(el_cardholder_full_name, 'CardholderLastName')
            el_cardholder_last_name.text = mapping_request.cardholder_full_name.cardholder_last_name
            el_address = ET.SubElement(el_create_mapping_request, 'Address')
            el_line1 = ET.SubElement(el_address, 'Line1')
            el_line1.text = mapping_request.address.line1
            el_line2 = ET.SubElement(el_address, 'Line2')
            el_line2.text = mapping_request.address.line2
            el_city = ET.SubElement(el_address, 'City')
            el_city.text = mapping_request.address.city
            el_country_subdivision = ET.SubElement(el_address, 'CountrySubdivision')
            el_country_subdivision.text = mapping_request.address.country_subdivision
            el_postal_code = ET.SubElement(el_address, 'PostalCode')
            el_postal_code.text = mapping_request.address.postal_code
            el_country = ET.SubElement(el_address, 'Country')
            el_country.text = mapping_request.address.country
            el_date_of_birth = ET.SubElement(el_create_mapping_request, 'DateOfBirth')
            el_date_of_birth.text = mapping_request.date_of_birth
            return ET.tostring(el_create_mapping_request, encoding="unicode")
        elif isinstance(mapping_request, inquiremappingrequest.InquireMappingRequest):
            el_inquire_mapping_request = ET.Element('InquireMappingRequest')
            el_subscriber_id = ET.SubElement(el_inquire_mapping_request, 'SubscriberId')
            el_subscriber_id.text = mapping_request.subscriber_id
            el_subscriber_type = ET.SubElement(el_inquire_mapping_request, 'SubscriberType')
            el_subscriber_type.text = mapping_request.subscriber_type
            el_account_usage = ET.SubElement(el_inquire_mapping_request, 'AccountUsage')
            el_account_usage.text = mapping_request.account_usage
            el_alias = ET.SubElement(el_inquire_mapping_request, 'Alias')
            el_alias.text = mapping_request.alias
            el_data_response_flag = ET.SubElement(el_inquire_mapping_request, 'DataResponseFlag')
            el_data_response_flag.text = mapping_request.data_response_flag
            return ET.tostring(el_inquire_mapping_request, encoding="unicode")
        elif isinstance(mapping_request, updatemappingrequest.UpdateMappingRequest):
            el_update_mapping_request = ET.Element('UpdateMappingRequest')
            el_account_usage = ET.SubElement(el_update_mapping_request, 'AccountUsage')
            el_account_usage.text = mapping_request.account_usage
            el_default_indicator = ET.SubElement(el_update_mapping_request, 'DefaultIndicator')
            el_default_indicator.text = mapping_request.default_indicator
            el_alias = ET.SubElement(el_update_mapping_request, 'Alias')
            el_alias.text = mapping_request.alias
            el_account_number = ET.SubElement(el_update_mapping_request, 'AccountNumber')
            el_account_number.text = mapping_request.account_number
            el_expiry_date = ET.SubElement(el_update_mapping_request, 'ExpiryDate')
            el_expiry_date.text = mapping_request.expiry_date
            el_cardholder_full_name = ET.Element('CardholderFullName')
            el_cardholder_first_name = ET.SubElement(el_cardholder_full_name, 'CardholderFirstName')
            el_cardholder_first_name.text = mapping_request.cardholder_full_name.cardholder_first_name
            el_cardholder_middle_name = ET.SubElement(el_cardholder_full_name, 'CardholderMiddleName')
            el_cardholder_middle_name.text = mapping_request.cardholder_full_name.cardholder_middle_name
            el_cardholder_last_name = ET.SubElement(el_cardholder_full_name, 'CardholderLastName')
            el_cardholder_last_name.text = mapping_request.cardholder_full_name.cardholder_last_name
            el_address = ET.Element('Address')
            el_line1 = ET.SubElement(el_address, 'Line1')
            el_line1.text = mapping_request.address.line1
            el_line2 = ET.SubElement(el_address, 'Line2')
            el_line2.text = mapping_request.address.line2
            el_city = ET.SubElement(el_address, 'City')
            el_city.text = mapping_request.address.city
            el_country_subdivision = ET.SubElement(el_address, 'CountrySubdivision')
            el_country_subdivision.text = mapping_request.address.country_subdivision
            el_postal_code = ET.SubElement(el_address, 'PostalCode')
            el_postal_code.text = mapping_request.address.postal_code
            el_country = ET.SubElement(el_address, 'Country')
            el_country.text = mapping_request.address.country
            el_date_of_birth = ET.SubElement(el_update_mapping_request, 'DateOfBirth')
            el_date_of_birth.text = mapping_request.date_of_birth
            return ET.tostring(el_update_mapping_request, encoding="unicode")

    def generate_return_object(self, xml_response):
        if xml_response.tag == 'CreateMapping':
            create_mapping = createmapping.CreateMapping()
            create_mapping.request_id = xml_response.find('RequestId').text
            tmp_mapping = mapping.Mapping()
            tmp_mapping.mapping_id = xml_response.find('Mapping/MappingId').text
            create_mapping.mapping = tmp_mapping
            return create_mapping
        elif xml_response.tag == 'InquireMapping':
            inquire_mapping = inquiremapping.InquireMapping()
            inquire_mapping.request_id = xml_response.find('RequestId').text

            mapping_array = list()
            for xml_mapping in xml_response.findall('.//Mapping'):
                tmp_mapping = mapping.Mapping()
                tmp_mapping.mapping_id = xml_mapping.find('MappingId').text
                tmp_mapping.subscriber_id = xml_mapping.find('SubscriberId').text
                tmp_mapping.account_usage = xml_mapping.find('AccountUsage').text
                tmp_mapping.default_indicator = xml_mapping.find('DefaultIndicator').text
                tmp_mapping.alias = xml_mapping.find('Alias').text
                tmp_mapping.ica = xml_mapping.find('ICA').text
                tmp_mapping.account_number = xml_mapping.find('AccountNumber').text

                tmp_cardholder_full_name = cardholderfullname.CardholderFullName()
                xml_cardholder_full_name = xml_mapping.find('CardholderFullName')
                tmp_cardholder_full_name.cardholder_first_name = xml_cardholder_full_name.find('CardholderFirstName').text
                tmp_cardholder_full_name.cardholder_middle_name = xml_cardholder_full_name.find('CardholderMiddleName').text
                tmp_cardholder_full_name.cardholder_last_name = xml_cardholder_full_name.find('CardholderLastName').text
                tmp_mapping.cardholder_full_name = tmp_cardholder_full_name

                tmp_address = address.Address()
                xml_address = xml_mapping.find('Address')
                tmp_address.line1 = xml_address.find('Line1').text
                tmp_address.line2 = xml_address.find('Line2').text
                tmp_address.city = xml_address.find('City').text
                tmp_address.postal_code = xml_address.find('PostalCode').text
                tmp_address.country_subdivision = xml_address.find('CountrySubdivision').text
                tmp_address.country = xml_address.find('Country').text
                tmp_mapping.address = tmp_address

                tmp_receiving_eligibility = receivingeligibility.ReceivingEligibility()
                xml_receiving_eligibility = xml_mapping.find('ReceivingEligibility')
                tmp_receiving_eligibility.eligible = xml_receiving_eligibility.find('Eligible').text
                tmp_currency = currency.Currency()
                xml_currency = xml_receiving_eligibility.find('Currency')
                tmp_currency.alpha_currency_code = xml_currency.find('AlphaCurrencyCode').text
                tmp_currency.numeric_currency_code = xml_currency.find('NumericCurrencyCode').text
                tmp_receiving_eligibility.currency = tmp_currency
                tmp_country = country.Country()
                xml_country = xml_receiving_eligibility.find('Country')
                tmp_country.alpha_country_code = xml_country.find('AlphaCountryCode').text
                tmp_country.numeric_country_code = xml_country.find('NumericCountryCode').text
                tmp_receiving_eligibility.country = tmp_country
                tmp_brand = brand.Brand()
                xml_brand = xml_receiving_eligibility.find('Brand')
                tmp_brand.acceptance_brand_code = xml_brand.find('AcceptanceBrandCode').text
                tmp_brand.product_brand_code = xml_brand.find('ProductBrandCode').text
                tmp_receiving_eligibility.brand = tmp_brand
                tmp_mapping.receiving_eligibility = tmp_receiving_eligibility

                tmp_mapping.expiry_date = xml_mapping.find('ExpiryDate').text

                mapping_array.append(tmp_mapping)
            tmp_mappings = mappings.Mappings(mapping_array)
            inquire_mapping.mappings = tmp_mappings
            return inquire_mapping
        elif xml_response.tag == 'UpdateMapping':
            update_mapping = updatemapping.UpdateMapping()
            update_mapping.request_id = xml_response.find('RequestId').text
            tmp_mapping = mapping.Mapping()
            tmp_mapping.mapping_id = xml_response.find('Mapping/MappingId').text
            update_mapping.mapping = tmp_mapping
            return update_mapping
        elif xml_response.tag == 'DeleteMapping':
            delete_mapping = deletemapping.DeleteMapping()
            delete_mapping.request_id = xml_response.find('RequestId').text
            tmp_mapping = mapping.Mapping()
            tmp_mapping.mapping_id = xml_response.find('Mapping/MappingId').text
            delete_mapping.mapping = tmp_mapping
            return delete_mapping