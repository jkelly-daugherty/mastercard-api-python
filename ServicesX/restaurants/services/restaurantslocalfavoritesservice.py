from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.restaurants.domain.restaurant import restaurants
from services.restaurants.domain.restaurant import restaurant
from services.restaurants.domain.restaurant import location
from services.restaurants.domain.restaurant import address
from services.restaurants.domain.restaurant import country
from services.restaurants.domain.restaurant import countrysubdivision
from services.restaurants.domain.restaurant import point

SANDBOX_URL = 'https://sandbox.api.mastercard.com/restaurants/v1/restaurant?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/restaurants/v1/restaurant?Format=XML'


class RestaurantLocalFavoritesService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_restaurants(self, options):
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
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()

        page_offset = xml_response.find('PageOffset').text
        total_count = xml_response.find('TotalCount').text

        restaurant_list = list()
        for xml_restaurant in xml_response.findall('.//Restaurant'):
            tmp_restaurant = restaurant.Restaurant()
            tmp_restaurant.id = none_check.verify_not_none(xml_restaurant.find('Id'))
            tmp_restaurant.name = none_check.verify_not_none(xml_restaurant.find('Name'))
            tmp_restaurant.website_url = none_check.verify_not_none(xml_restaurant.find('WebsiteUrl'))
            tmp_restaurant.phone_number = none_check.verify_not_none(xml_restaurant.find('PhoneNumber'))
            tmp_restaurant.category = none_check.verify_not_none(xml_restaurant.find('Category'))
            tmp_restaurant.local_favorite_ind = none_check.verify_not_none(xml_restaurant.find('LocalFavoriteInd'))
            tmp_restaurant.hidden_gem_ind = none_check.verify_not_none(xml_restaurant.find('HiddenGemInd'))

            xml_location = xml_restaurant.find('Location')
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
            tmp_restaurant.location = tmp_location

            restaurant_list.append(tmp_restaurant)
        restaurants_ = restaurants.Restaurants(page_offset, total_count, restaurant_list)
        return restaurants_