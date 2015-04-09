class PaymentRequest(object):

    def __init__(self):
        self.local_date = ''
        self.local_time = ''
        self.transaction_reference = ''
        self.sender_name = ''
        self.sender_address = ''
        self.receiving_card = ''
        self.receiving_mapped = ''
        self.receiving_amount = ''
        self.ica = ''
        self.processor_id = ''
        self.routing_and_transit_number = ''
        self.card_acceptor = ''
        self.transaction_desc = ''
        self.merchant_id = ''