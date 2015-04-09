import re

class TerminationInquiry(object):
    def __init__(self, page_offset, total_length, ref, terminated_merchant):
        self.page_offset = page_offset
        self.page_length = total_length
        self.ref = ref
        self.transaction_reference_number = ''
        self.terminated_merchant = terminated_merchant

    def get_reference_id(self):
        if self.ref is not None:
            irn = re.search('([^\/]+)$', self.ref)
            return irn.group(1)
        else:
            return ''