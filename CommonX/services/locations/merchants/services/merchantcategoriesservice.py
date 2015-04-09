from common import connector
from common import urlutil
from common import environment
from services.locations.domain.categories import categories
from services.locations.domain.categories import category
import xml.etree.ElementTree as ET

SANDBOX_URL = 'https://sandbox.api.mastercard.com/merchants/v1/category?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/merchants/v1/category?Format=XML'


class MerchantCategoryService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_categories(self):
        url = self.get_url()
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL
        return url

    def generate_return_object(self, xml_response):
        category_list = list()
        for xml_category in xml_response.findall('Category'):
            tmp_category = category.Category(xml_category.text)
            category_list.append(tmp_category)
        categories_ = categories.Categories(category_list)
        return categories_