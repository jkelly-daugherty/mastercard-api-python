from common import connector
from common import environment
from common import xmlutil
from services.restaurants.domain.countries import country
from services.restaurants.domain.countries import countries
import xml.etree.ElementTree as ET

SANDBOX_URL = 'https://sandbox.api.mastercard.com/restaurants/v1/country?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/restaurants/v1/country?Format=XML'


class CountriesLocalFavoritesService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_countries(self):
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()
        country_list = list()
        for xml_country in xml_response.findall('Country'):
            tmp_country = country.Country(
                none_check.verify_not_none(xml_country.find('Name')),
                none_check.verify_not_none(xml_country.find('Code'))
            )
            tmp_country.geo_coding = none_check.verify_not_none(xml_country.find('GeoCoding'))
            country_list.append(tmp_country)
        countries_ = countries.Countries(country_list)
        return countries_