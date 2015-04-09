class TerminationInquiryRequestOptions(object):
    def __init__(self, page_offset, page_length):
        self.page_offset = page_offset
        self.page_length = page_length
        if self.page_length > 25:
            self.page_length = 25