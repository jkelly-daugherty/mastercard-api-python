class Restaurants(object):

    def __init__(self, page_offset, total_count, restaurant):
        self.page_offset = page_offset
        self.total_count = total_count
        self.restaurant = restaurant