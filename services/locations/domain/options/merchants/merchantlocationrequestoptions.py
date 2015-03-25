class MerchantLocationRequestOptions(object):

    KILOMETER = 'KILOMETER'
    MILE = 'MILE'

    def __init__(self, details, page_offset, page_length):
        self.details = details
        self.page_offset = page_offset
        self.page_length = page_length
        self.category = ''
        self.address_line1 = ''
        self.address_line2 = ''
        self.city = ''
        self.country_subdivision = ''
        self.postal_code = ''
        self.country = ''
        self.latitude = ''
        self.longitude = ''
        self.distance_unit = ''
        self.radius = ''
        self.offer_merchant_id = ''