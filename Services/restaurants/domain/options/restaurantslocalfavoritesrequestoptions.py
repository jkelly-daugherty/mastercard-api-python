class RestaurantsLocalFavoritesRequestOptions(object):

    KILOMETER = 'KILOMETER'
    MILE = 'MILE'

    def __init__(self, page_offset, page_length):
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
        if self.page_length > 25:
            self.page_length = 25