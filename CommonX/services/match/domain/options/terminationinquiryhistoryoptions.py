class TerminationInquiryHistoryOptions(object):
    def __init__(self, page_offset, page_length, acquirer_id, inquiry_reference_number):
        self.page_offset = page_offset
        self.page_length = page_length
        self.acquirer_id = acquirer_id
        self.inquiry_reference_number = inquiry_reference_number
        if self.page_length > 25:
            self.page_length = 25