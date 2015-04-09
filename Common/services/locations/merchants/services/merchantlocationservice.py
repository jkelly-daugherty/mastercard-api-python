from common import connector
from common import urlutil
from common import environment
from common import xmlutil
import xml.etree.ElementTree as ET
from services.locations.domain.merchants import merchant
from services.locations.domain.merchants import merchants
from services.locations.domain.merchants import acceptance
from services.locations.domain.merchants import location
from services.locations.domain.merchants import cashback
from services.locations.domain.merchants import features
from services.locations.domain.merchants import topup
from services.locations.domain.merchants import paypass
from services.locations.domain.merchants import repower
from services.locations.domain.merchants import products
from services.locations.domain.common.countries import country
from services.locations.domain.common.country_subdivisions import countrysubdivision
from services.locations.domain.common import point
from services.locations.domain.common import address

SANDBOX_URL = 'https://sandbox.api.mastercard.com/merchants/v1/merchant?Format=XML'
PRODUCTION_URL = 'https://api.mastercard.com/merchants/v1/merchant?Format=XML'


class MerchantLocationService(connector.Connector):
    def __init__(self, consumer_key, private_key, environment):
        super().__init__(consumer_key, private_key)
        self.environment = environment

    def get_merchants(self, options):
        url = self.get_url(options)
        xml_response = ET.fromstring(self.do_request(url, 'GET'))
        return self.generate_return_object(xml_response)

    def get_url(self, options):
        url = SANDBOX_URL
        if self.environment == environment.Environment.PRODUCTION:
            url = PRODUCTION_URL

        url = urlutil.UrlUtil.add_query_parameter(url, "Details", options.details)
        url = urlutil.UrlUtil.add_query_parameter(url, "PageOffset", options.page_offset)
        url = urlutil.UrlUtil.add_query_parameter(url, "PageLength", options.page_length)
        url = urlutil.UrlUtil.add_query_parameter(url, "Category", options.category)
        url = urlutil.UrlUtil.add_query_parameter(url, "AddressLine1", options.address_line1)
        url = urlutil.UrlUtil.add_query_parameter(url, "AddressLine2", options.address_line2)
        url = urlutil.UrlUtil.add_query_parameter(url, "City", options.city)
        url = urlutil.UrlUtil.add_query_parameter(url, "CountrySubdivision", options.country_subdivision)
        url = urlutil.UrlUtil.add_query_parameter(url, "PostalCode", options.postal_code)
        url = urlutil.UrlUtil.add_query_parameter(url, "Country", options.country.name)
        url = urlutil.UrlUtil.add_query_parameter(url, "Latitude", options.latitude)
        url = urlutil.UrlUtil.add_query_parameter(url, "Longitude", options.longitude)
        url = urlutil.UrlUtil.add_query_parameter(url, "DistanceUnit", options.distance_unit)
        url = urlutil.UrlUtil.add_query_parameter(url, "Radius", options.radius)
        url = urlutil.UrlUtil.add_query_parameter(url, "OfferMerchantId", options.offer_merchant_id)
        return url

    def generate_return_object(self, xml_response):
        none_check = xmlutil.XMLUtil()

        page_offset = xml_response.find('PageOffset').text
        total_count = xml_response.find('TotalCount').text

        merchant_list = list()
        for xml_merchant in xml_response.findall('.//Merchant'):
            tmp_merchant = merchant.Merchant()
            tmp_merchant.id = none_check.verify_not_none(xml_merchant.find('Id'))
            tmp_merchant.name = none_check.verify_not_none(xml_merchant.find('Name'))
            tmp_merchant.website_url = none_check.verify_not_none(xml_merchant.find('WebsiteUrl'))
            tmp_merchant.phone_number = none_check.verify_not_none(xml_merchant.find('PhoneNumber'))
            tmp_merchant.category = none_check.verify_not_none(xml_merchant.find('Category'))

            xml_location = xml_merchant.find('Location')
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

            xml_country_subdivision = xml_address.find('CountrySubdivision')
            tmp_country_subdivision = countrysubdivision.CountrySubdivision(
                none_check.verify_not_none(xml_country_subdivision.find('Name')),
                none_check.verify_not_none(xml_country_subdivision.find('Code'))
            )
            tmp_address.country_subdivision = tmp_country_subdivision

            xml_country = xml_address.find('Country')
            tmp_country = country.Country(
                none_check.verify_not_none(xml_country.find('Name')),
                none_check.verify_not_none(xml_country.find('Code')))
            tmp_address.country = tmp_country

            xml_point = xml_location.find('Point')
            tmp_point = point.Point(
                none_check.verify_not_none(xml_point.find('Latitude')),
                none_check.verify_not_none(xml_point.find('Longitude')))
            tmp_location.point = tmp_point

            if xml_merchant.find('Topup') is not None:
                tmp_repower = repower.RePower(
                    none_check.verify_not_none(xml_merchant.find('Topup/RePower/CardSwipe')),
                    none_check.verify_not_none(xml_merchant.find('Topup/RePower/MoneyPak'))
                )
                tmp_topup = topup.Topup(tmp_repower)
                tmp_merchant.topup = tmp_topup

            if xml_merchant.find('Products') is not None:
                xml_products = xml_merchant.find('Products')
                tmp_products = products.Products(none_check.verify_not_none(xml_products.find('PrepaidTravelCard')))
                tmp_merchant.products = tmp_products

            if xml_merchant.find('Features') is not None:
                xml_features = xml_merchant.find('Features')
                tmp_cash_back = cashback.CashBack(none_check.verify_not_none(xml_features.find('CashBack/MaximumAmount')))
                tmp_features = features.Features(tmp_cash_back)
                tmp_merchant.features = tmp_features

            # At time of testing, Acceptance data was not returning as described in the documentation.
            # Uncomment when data is corrected.

            # xml_acceptance = xml_merchant.find('Acceptance')
            # xml_pay_pass = xml_acceptance.find('PayPass')
            # tmp_pay_pass = paypass.PayPass()
            # tmp_pay_pass.concession = none_check.verify_not_none(xml_pay_pass.find('Concession'))
            # tmp_pay_pass.pharmacy = none_check.verify_not_none(xml_pay_pass.find('Pharmacy'))
            # tmp_pay_pass.fuel_pump = none_check.verify_not_none(xml_pay_pass.find('FuelPump'))
            # tmp_pay_pass.toll_booth = none_check.verify_not_none(xml_pay_pass.find('TollBooth'))
            # tmp_pay_pass.drive_thru = none_check.verify_not_none(xml_pay_pass.find('DriveThru'))
            # tmp_pay_pass.register = none_check.verify_not_none(xml_pay_pass.find('Register'))
            # tmp_pay_pass.ticketing = none_check.verify_not_none(xml_pay_pass.find('Ticketing'))
            # tmp_pay_pass.vending_machine = none_check.verify_not_none(xml_pay_pass.find('VendingMachine'))
            # tmp_acceptance = acceptance.Acceptance(tmp_pay_pass)
            # tmp_merchant.acceptance = tmp_acceptance

            merchant_list.append(tmp_merchant)
        merchants_ = merchants.Merchants(merchant_list, page_offset, total_count)
        return merchants_