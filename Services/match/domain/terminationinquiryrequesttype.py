class TerminationInquiryRequestType(object):
    def __init__(self, acquirer_id, merchant):
        self.acquirer_id = acquirer_id
        self.transaction_reference_number = ''
        self.merchant = merchant
