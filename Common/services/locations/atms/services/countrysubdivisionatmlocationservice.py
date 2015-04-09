from common import connector
from common import urlutil
from common import environment
from common import xmlutil
from services.locations.domain.common.country_subdivisions import countrysubdivision
from services.locations.domain.common.country_subdivisions import countrysubdivisions
import xml.etree.ElementTree as ET

SANDBOX_URL = 'https://sandbox.api.mastercard.com/atms/v1/countrysubdivision?Format=XML'
PRODUCTION_URL = 'https://sandbox.api.mastercard.com/atms/v1/countrysubdivision?Format=XML'


class CountrySubdivisionAtmLocationService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_country_subdivisions(self, options):
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self, options):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        url = urlutil.UrlUtil.add_query_parameter(url, 'Country', options.country)
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        country_subdivision_list = list()
        for xml_country_subdivision in xml_response.findall('CountrySubdivision'):
            tmp_country_subdivision = countrysubdivision.CountrySubdivision(
                none_check.verify_not_none(xml_country_subdivision.find('Name')),
                none_check.verify_not_none(xml_country_subdivision.find('Code'))
            )
            country_subdivision_list.append(tmp_country_subdivision)
        country_subdivisions = countrysubdivisions.CountrySubdivisions(country_subdivision_list)
        return country_subdivisions