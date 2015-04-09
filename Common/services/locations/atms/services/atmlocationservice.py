from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.locations.domain.atms import atm
from services.locations.domain.atms import atms
from services.locations.domain.atms import location
from services.locations.domain.common import address
from services.locations.domain.common.countries import country
from services.locations.domain.common.country_subdivisions import countrysubdivision
from services.locations.domain.common import point

SANDBOX_URL = 'https://sandbox.api.mastercard.com/atms/v1/atm?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/atms/v1/atm?Format=XML'


class AtmLocationService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_atms(self, options):
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self, options):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL

        url = urlutil.UrlUtil.add_query_parameter(url, 'PageOffset', options.page_offset)
        url = urlutil.UrlUtil.add_query_parameter(url, 'PageLength', options.page_length)
        url = urlutil.UrlUtil.add_query_parameter(url, 'Category', options.category)
        url = urlutil.UrlUtil.add_query_parameter(url, 'AddressLine1', options.address_line1)
        url = urlutil.UrlUtil.add_query_parameter(url, 'AddressLine2', options.address_line2)
        url = urlutil.UrlUtil.add_query_parameter(url, 'City', options.city)
        url = urlutil.UrlUtil.add_query_parameter(url, 'CountrySubdivision', options.country_subdivision)
        url = urlutil.UrlUtil.add_query_parameter(url, 'PostalCode', options.postal_code)
        url = urlutil.UrlUtil.add_query_parameter(url, 'Country', options.country)
        url = urlutil.UrlUtil.add_query_parameter(url, 'Latitude', options.latitude)
        url = urlutil.UrlUtil.add_query_parameter(url, 'Longitude', options.longitude)
        url = urlutil.UrlUtil.add_query_parameter(url, 'DistanceUnit', options.distance_unit)
        url = urlutil.UrlUtil.add_query_parameter(url, 'Radius', options.radius)
        url = urlutil.UrlUtil.add_query_parameter(url, 'SupportEMV', options.support_emv)
        url = urlutil.UrlUtil.add_query_parameter(url, 'InternationalMaestroAccepted', options.international_maestro_accepted)
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()

        page_offset = xml_response.find('PageOffset').text
        total_count = xml_response.find('TotalCount').text

        atm_list = list()
        for xml_atm in xml_response.findall('.//Atm'):
            tmp_atm = atm.Atm()
            tmp_atm.handicap_accessible = none_check.verify_not_none(xml_atm.find('HandicapAccessable'))
            tmp_atm.camera = none_check.verify_not_none(xml_atm.find('Camera'))
            tmp_atm.availability = none_check.verify_not_none(xml_atm.find('Availability'))
            tmp_atm.access_fees = none_check.verify_not_none(xml_atm.find('AccessFees'))
            tmp_atm.owner = none_check.verify_not_none(xml_atm.find('Owner'))
            tmp_atm.shared_deposit = none_check.verify_not_none(xml_atm.find('SharedDeposit'))
            tmp_atm.surcharge_free_alliance = none_check.verify_not_none(xml_atm.find('SurchargeFreeAlliance'))
            tmp_atm.sponsor = none_check.verify_not_none(xml_atm.find('Sponsor'))
            tmp_atm.support_emv = none_check.verify_not_none(xml_atm.find('SupportEMV'))
            tmp_atm.surcharge_free_alliance_network = none_check.verify_not_none(xml_atm.find('SurchargeFreeAllianceNetwork'))

            xml_location = xml_atm.find('Location')
            tmp_location = location.Location()
            tmp_location.name = none_check.verify_not_none(xml_location.find('Name'))
            tmp_location.distance = none_check.verify_not_none(xml_location.find('Distance'))
            tmp_location.distance_unit = none_check.verify_not_none(xml_location.find('DistanceUnit'))

            xml_address = xml_location.find('Address')
            tmp_address = address.Address()
            tmp_address.line1 = none_check.verify_not_none(xml_address.find('Line1'))
            tmp_address.line2 = none_check.verify_not_none(xml_address.find('Line2'))
            tmp_address.city = none_check.verify_not_none(xml_address.find('City'))
            tmp_address.postal_code = none_check.verify_not_none(xml_address.find('PostalCode'))

            tmp_country = country.Country(
                none_check.verify_not_none(xml_address.find('Country/Name')),
                none_check.verify_not_none(xml_address.find('Country/Code'))
            )

            tmp_country_subdivision = countrysubdivision.CountrySubdivision(
                none_check.verify_not_none(xml_address.find('CountrySubdivision/Name')),
                none_check.verify_not_none(xml_address.find('CountrySubdivision/Code'))
            )

            tmp_address.country = tmp_country
            tmp_address.country_subdivision = tmp_country_subdivision

            xml_point = xml_location.find('Point')
            tmp_point = point.Point(
                none_check.verify_not_none(xml_point.find('Latitude')),
                none_check.verify_not_none(xml_point.find('Longitude'))
            )

            tmp_location.point = tmp_point
            tmp_location.address = tmp_address
            tmp_atm.location = tmp_location

            atm_list.append(tmp_atm)
        atms_ = atms.Atms(page_offset, total_count, atm_list)
        return atms_