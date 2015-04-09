class AtmLocationRequestOptions(object):

    KILOMETER = 'KILOMETER'
    MILE = 'MILE'
    SUPPORT_EMV_YES = 1
    SUPPORT_EMV_NO = 2
    SUPPORT_EMV_UNKNOWN = 0
    INTERNATIONAL_MAESTRO_ACCEPTED_YES = 1

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
        self.support_emv = ''
        self.international_maestro_accepted = ''