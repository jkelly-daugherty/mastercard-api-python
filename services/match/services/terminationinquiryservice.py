from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.match.domain import terminationinquiry
from services.match.domain import driverslicensetype
from services.match.domain import addresstype
from services.match.domain import principaltype
from services.match.domain import terminatedmerchanttype
from services.match.domain import merchantmatchtype
from services.match.domain import merchanttype
from services.match.domain import principalmatchtype

SANDBOX_URL = 'https://sandbox.api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/fraud/merchant/v1/termination-inquiry?Format=XML'


class TerminationInquiryService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_termination_inquiry(self, termination_inquiry_request, options):
        body = self.generate_xml(termination_inquiry_request)
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'POST', body))
        return self.generate_return_object(xml_response)

    def get_url(self, options):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        url = urlutil.UrlUtil.add_query_parameter(url, "PageOffset", options.page_offset)
        url = urlutil.UrlUtil.add_query_parameter(url, "PageLength", options.page_length)
        return url

    def generate_xml(self, termination_inquiry_request):
        el_termination_inquiry_request = ET.Element('TerminationInquiryRequest')
        el_acquirer_id = ET.SubElement(el_termination_inquiry_request, 'AcquirerId')
        el_acquirer_id.text = termination_inquiry_request.acquirer_id
        el_transaction_reference_number = ET.SubElement(el_termination_inquiry_request, 'TransactionReferenceNumber')
        el_transaction_reference_number.text = termination_inquiry_request.transaction_reference_number
        el_merchant = ET.SubElement(el_termination_inquiry_request, 'Merchant')
        el_merchant_name = ET.SubElement(el_merchant, 'Name')
        el_merchant_name.text = termination_inquiry_request.merchant.name
        el_merchant_business_name = ET.SubElement(el_merchant, 'DoingBusinessAsName')
        el_merchant_business_name.text = termination_inquiry_request.merchant.doing_business_as_name
        el_merchant_phone_number = ET.SubElement(el_merchant, 'PhoneNumber')
        el_merchant_phone_number.text = termination_inquiry_request.merchant.phone_number
        el_merchant_address = ET.SubElement(el_merchant, 'Address')
        el_merchant_address_line1 = ET.SubElement(el_merchant_address, 'Line1')
        el_merchant_address_line1.text = termination_inquiry_request.merchant.address.line1
        el_merchant_address_line2 = ET.SubElement(el_merchant_address, 'Line2')
        el_merchant_address_line2.text = termination_inquiry_request.merchant.address.line2
        el_merchant_address_city = ET.SubElement(el_merchant_address, 'City')
        el_merchant_address_city.text = termination_inquiry_request.merchant.address.city
        el_merchant_address_country_sub = ET.SubElement(el_merchant_address, 'CountrySubdivision')
        el_merchant_address_country_sub.text = termination_inquiry_request.merchant.address.country_subdivision
        el_merchant_address_postal_code = ET.SubElement(el_merchant_address, 'PostalCode')
        el_merchant_address_postal_code.text = termination_inquiry_request.merchant.address.postal_code
        el_merchant_address_country = ET.SubElement(el_merchant_address, 'Country')
        el_merchant_address_country.text = termination_inquiry_request.merchant.address.country
        el_merchant_cs_tax = ET.SubElement(el_merchant, 'CountrySubdivisionTaxId')
        el_merchant_cs_tax.text = termination_inquiry_request.merchant.country_subdivision_tax_id
        el_merchant_national_tax = ET.SubElement(el_merchant, 'NationalTaxId')
        el_merchant_national_tax.text = termination_inquiry_request.merchant.national_tax_id
        el_principal = ET.SubElement(el_merchant, 'Principal')
        el_principal_first_name = ET.SubElement(el_principal, 'FirstName')
        el_principal_first_name.text = termination_inquiry_request.merchant.principal.first_name
        el_principal_last_name = ET.SubElement(el_principal, 'LastName')
        el_principal_last_name.text = termination_inquiry_request.merchant.principal.last_name
        el_principal_national_id = ET.SubElement(el_principal, 'NationalId')
        el_principal_national_id.text = termination_inquiry_request.merchant.principal.national_id
        el_principal_phone_number = ET.SubElement(el_principal, 'PhoneNumber')
        el_principal_phone_number.text = termination_inquiry_request.merchant.principal.phone_number
        el_principal_address = ET.SubElement(el_principal, 'Address')
        el_principal_address_line1 = ET.SubElement(el_principal_address, 'Line1')
        el_principal_address_line1.text = termination_inquiry_request.merchant.principal.address.line1
        el_principal_address_line2 = ET.SubElement(el_principal_address, 'Line2')
        el_principal_address_line2.text = termination_inquiry_request.merchant.principal.address.line2
        el_principal_address_city = ET.SubElement(el_principal_address, 'City')
        el_principal_address_city.text = termination_inquiry_request.merchant.principal.address.city
        el_principal_address_country_sub = ET.SubElement(el_principal_address, 'CountrySubdivision')
        el_principal_address_country_sub.text = termination_inquiry_request.merchant.principal.address.country_subdivision
        el_principal_address_postal_code = ET.SubElement(el_principal_address, 'PostalCode')
        el_principal_address_postal_code.text = termination_inquiry_request.merchant.principal.address.postal_code
        el_principal_address_country = ET.SubElement(el_principal_address, 'Country')
        el_principal_address_country.text = termination_inquiry_request.merchant.principal.address.country
        el_principal_drivers_license = ET.SubElement(el_principal, 'DriversLicense')
        el_principal_drivers_license_number = ET.SubElement(el_principal_drivers_license, 'Number')
        el_principal_drivers_license_number.text = termination_inquiry_request.merchant.principal.drivers_license.number
        el_principal_drivers_license_country_subdivision = ET.SubElement(el_principal_drivers_license, 'CountrySubdivision')
        el_principal_drivers_license_country_subdivision.text = termination_inquiry_request.merchant.principal.drivers_license.country_subdivision
        el_principal_drivers_license_country = ET.SubElement(el_principal_drivers_license, 'Country')
        el_principal_drivers_license_country.text = termination_inquiry_request.merchant.principal.drivers_license.country
        body = ET.tostring(el_termination_inquiry_request, encoding="unicode")
        body = body.replace('<TerminationInquiryRequest>', '<ns2:TerminationInquiryRequest xmlns:ns2="http://mastercard.com/termination">')
        body = body.replace('</TerminationInquiryRequest>', '</ns2:TerminationInquiryRequest>')
        return body

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()

        page_offset = none_check.verify_not_none(xml_response.find('PageOffset'))
        total_length = none_check.verify_not_none(xml_response.find('TotalLength'))
        ref = none_check.verify_not_none(xml_response.find('Ref'))
        transaction_reference_number = none_check.verify_not_none(xml_response.find('TransactionReferenceNumber'))

        terminated_merchant_list = list()
        for xml_terminated_merchant in xml_response.findall('TerminatedMerchant'):
            terminated_merchant = terminatedmerchanttype.TerminatedMerchantType()
            terminated_merchant.termination_reason_code = none_check.verify_not_none(xml_terminated_merchant.find('TerminationReasonCode'))

            xml_merchant = xml_terminated_merchant.find('Merchant')
            merchant_type = merchanttype.MerchantType()
            merchant_type.name = none_check.verify_not_none(xml_merchant.find('Name'))
            merchant_type.doing_business_as_name = none_check.verify_not_none(xml_merchant.find('DoingBusinessAsName'))
            merchant_type.phone_number = none_check.verify_not_none(xml_merchant.find('PhoneNumber'))

            xml_merchant_address = xml_merchant.find('Address')
            merchant_address = addresstype.AddressType()
            merchant_address.line1 = none_check.verify_not_none(xml_merchant_address.find('Line1'))
            merchant_address.line2 = none_check.verify_not_none(xml_merchant_address.find('Line2'))
            merchant_address.city = none_check.verify_not_none(xml_merchant_address.find('City'))
            merchant_address.country_subdivision = none_check.verify_not_none(xml_merchant_address.find('CountrySubdivision'))
            merchant_address.postal_code = none_check.verify_not_none(xml_merchant_address.find('PostalCode'))
            merchant_address.country = none_check.verify_not_none(xml_merchant_address.find('Country'))
            merchant_type.address = merchant_address

            principal_list = list()
            for xml_principal in xml_merchant.findall('Principal'):
                principal_type = principaltype.PrincipalType()
                principal_type.first_name = none_check.verify_not_none(xml_principal.find('FirstName'))
                principal_type.last_name = none_check.verify_not_none(xml_principal.find('LastName'))
                principal_type.national_id = none_check.verify_not_none(xml_principal.find('NationalId'))
                principal_type.phone_number = none_check.verify_not_none(xml_principal.find('PhoneNumber'))

                xml_principal_address = xml_principal.find('Address')
                principal_address = addresstype.AddressType()
                principal_address.line1 = none_check.verify_not_none(xml_principal_address.find('Line1'))
                principal_address.line2 = none_check.verify_not_none(xml_principal_address.find('Line2'))
                principal_address.city = none_check.verify_not_none(xml_principal_address.find('City'))
                principal_address.country_subdivision = none_check.verify_not_none(xml_principal_address.find('CountrySubdivision'))
                principal_address.postal_code = none_check.verify_not_none(xml_principal_address.find('PostalCode'))
                principal_address.country = none_check.verify_not_none(xml_principal_address.find('Country'))

                xml_drivers_license = xml_principal.find('DriversLicense')
                drivers_license = driverslicensetype.DriversLicenseType()
                drivers_license.number = none_check.verify_not_none(xml_drivers_license.find('Number'))
                drivers_license.country_subdivision = none_check.verify_not_none(xml_drivers_license.find('CountrySubdivision'))
                drivers_license.country = none_check.verify_not_none(xml_drivers_license.find('Country'))
                principal_type.drivers_license = drivers_license
                principal_type.address = principal_address
                principal_list.append(principal_type)
            merchant_type.principal = principal_list
            terminated_merchant.merchant = merchant_type

            xml_merchant_match = xml_terminated_merchant.find('MerchantMatch')
            merchant_match = merchantmatchtype.MerchantMatchType()
            merchant_match.name = none_check.verify_not_none(xml_merchant_match.find('Name'))
            merchant_match.doing_business_as_name = none_check.verify_not_none(xml_merchant_match.find('DoingBusinessAsName'))
            merchant_match.phone_number = none_check.verify_not_none(xml_merchant_match.find('PhoneNumber'))
            merchant_match.address = none_check.verify_not_none(xml_merchant_match.find('Address'))
            merchant_match.country_subdivision_tax_id = none_check.verify_not_none(xml_merchant_match.find('CountrySubdivisionTaxId'))
            merchant_match.national_tax_id = none_check.verify_not_none(xml_merchant_match.find('NationalTaxId'))

            principal_match_list = list()
            for xml_principal_match in xml_merchant_match.findall('PrincipalMatch'):
                principal_match_type = principalmatchtype.PrincipalMatchType()
                principal_match_type.name = none_check.verify_not_none(xml_principal_match.find('Name'))
                principal_match_type.national_id = none_check.verify_not_none(xml_principal_match.find('NationalId'))
                principal_match_type.phone_number = none_check.verify_not_none(xml_principal_match.find('PhoneNumber'))
                principal_match_type.address = none_check.verify_not_none(xml_principal_match.find('Address'))
                principal_match_type.drivers_license = none_check.verify_not_none(xml_principal_match.find('DriversLicense'))
                principal_match_list.append(principal_match_type)

            merchant_match.principal_match = principal_match_list
            terminated_merchant.merchant_match = merchant_match
            terminated_merchant_list.append(terminated_merchant)

        termination_inquiry = terminationinquiry.TerminationInquiry(page_offset, total_length, ref, terminated_merchant_list)
        termination_inquiry.transaction_reference_number = transaction_reference_number
        return termination_inquiry
