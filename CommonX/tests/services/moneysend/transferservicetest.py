import unittest
import random
from tests import testutils
from common import environment
from tests import testconstants
from services.moneysend.services import transferservice
from services.moneysend.domain.transfer import transferrequest
from services.moneysend.domain.transfer import paymentrequest
from services.moneysend.domain.transfer import senderaddress
from services.moneysend.domain.transfer import fundingcard
from services.moneysend.domain.transfer import receiveraddress
from services.moneysend.domain.transfer import receivingamount
from services.moneysend.domain.transfer import cardacceptor
from services.moneysend.domain.transfer import fundingmapped
from services.moneysend.domain.transfer import fundingamount
from services.moneysend.domain.transfer import receivingmapped
from services.moneysend.domain.transfer import receivingcard


class TransferServiceTest(unittest.TestCase):
    def setUp(self):
        test_utils = testutils.TestUtils(environment.Environment.SANDBOX)
        self._service = transferservice.TransferService(testconstants.TestConstants.SANDBOX_CONSUMER_KEY,
                                                        test_utils.get_private_key(),
                                                        environment.Environment.SANDBOX)

    def test_transfer_request_card_test(self):
        transfer_request_card = transferrequest.TransferRequest()
        transfer_request_card.local_date = '1212'
        transfer_request_card.local_time = '161222'
        transfer_request_card.transaction_reference = self.trans_ref_num(19)
        transfer_request_card.sender_name = 'John Doe'

        sender_address = senderaddress.SenderAddress()
        sender_address.line1 = '123 Main Street'
        sender_address.line2 = '#5A'
        sender_address.city = 'Arlington'
        sender_address.country_subdivision = 'VA'
        sender_address.postal_code = '22207'
        sender_address.country = 'USA'
        transfer_request_card.sender_address = sender_address

        funding_card = fundingcard.FundingCard()
        funding_card.account_number = '5184680430000006'
        funding_card.expiry_month = '11'
        funding_card.expiry_year = '2014'
        transfer_request_card.funding_card = funding_card

        transfer_request_card.funding_ucaf = 'MjBjaGFyYWN0ZXJqdW5rVUNBRjU=1111'
        transfer_request_card.funding_mastercard_assigned_id = '123456'

        funding_amount = fundingamount.FundingAmount()
        funding_amount.value = '12000'
        funding_amount.currency = '840'
        transfer_request_card.funding_amount = funding_amount

        transfer_request_card.receiver_name = 'Jose Lopez'

        receiver_address = receiveraddress.ReceiverAddress()
        receiver_address.line1 = 'Pueblo Street'
        receiver_address.line2 = 'PO BOX 12'
        receiver_address.city = 'El PASO'
        receiver_address.country_subdivision = 'TX'
        receiver_address.postal_code = '79906'
        receiver_address.country = 'USA'
        transfer_request_card.receiver_address = receiver_address

        transfer_request_card.receiver_phone = '1800639426'

        receiving_card = receivingcard.ReceivingCard()
        receiving_card.account_number = '5184680430000006'
        transfer_request_card.receiving_card = receiving_card

        receiving_amount = receivingamount.ReceivingAmount()
        receiving_amount.value = '182206'
        receiving_amount.currency = '484'
        transfer_request_card.receiving_amount = receiving_amount

        transfer_request_card.channel = 'W'
        transfer_request_card.ucaf_support = 'false'
        transfer_request_card.ica = '009674'
        transfer_request_card.processor_id = '9000000442'
        transfer_request_card.routing_and_transit_number = '990442082'

        card_acceptor = cardacceptor.CardAcceptor()
        card_acceptor.name = 'My Local Bank'
        card_acceptor.city = 'Saint Louis'
        card_acceptor.state = 'MO'
        card_acceptor.postal_code = '63101'
        card_acceptor.country = 'USA'
        transfer_request_card.card_acceptor = card_acceptor

        transfer_request_card.transaction_desc = 'P2P'
        transfer_request_card.merchant_id = '123456'

        transfer_ = self._service.get_transfer(transfer_request_card)
        assert transfer_.transaction_reference is not None and int(transfer_.transaction_reference) > 0
        assert transfer_.transaction_history.transaction[0] is not None
        assert int(transfer_.transaction_history.transaction[0].response.code) == 00
        assert int(transfer_.transaction_history.transaction[1].response.code) == 00

    def test_transfer_request_mapped_test(self):
        transfer_request_mapped = transferrequest.TransferRequest()
        transfer_request_mapped.local_date = '1212'
        transfer_request_mapped.local_time = '161222'
        transfer_request_mapped.transaction_reference = self.trans_ref_num(19)
    
        funding_mapped = fundingmapped.FundingMapped()
        funding_mapped.subscriber_id = 'examplePythonSending2@email.com'
        funding_mapped.subscriber_type = 'EMAIL_ADDRESS'
        funding_mapped.subscriber_alias = 'My Debit Card'
        transfer_request_mapped.funding_mapped = funding_mapped
    
        transfer_request_mapped.funding_ucaf = 'MjBjaGFyYWN0ZXJqdW5rVUNBRjU=1111'
        transfer_request_mapped.funding_mastercard_assigned_id = '123456'
    
        funding_amount = fundingamount.FundingAmount()
        funding_amount.value = '15000'
        funding_amount.currency = '840'
        transfer_request_mapped.funding_amount = funding_amount
    
        transfer_request_mapped.receiver_name = 'Jose Lopez'
    
        receiver_address = receiveraddress.ReceiverAddress()
        receiver_address.line1 = 'Pueblo Street'
        receiver_address.line2 = 'PO BOX 12'
        receiver_address.city = 'El PASO'
        receiver_address.country_subdivision = 'TX'
        receiver_address.postal_code = '79906'
        receiver_address.country = 'USA'
        transfer_request_mapped.receiver_address = receiver_address
    
        transfer_request_mapped.receiver_phone = '1800639426'
    
        receiving_card = receivingcard.ReceivingCard()
        receiving_card.account_number = '5184680430000014'
        transfer_request_mapped.receiving_card = receiving_card
    
        receiving_amount = receivingamount.ReceivingAmount()
        receiving_amount.value = '182206'
        receiving_amount.currency = '484'
        transfer_request_mapped.receiving_amount = receiving_amount
    
        transfer_request_mapped.channel = 'W'
        transfer_request_mapped.ucaf_support = 'false'
        transfer_request_mapped.ica = '009674'
        transfer_request_mapped.processor_id = '9000000442'
        transfer_request_mapped.routing_and_transit_number = '990442082'
    
        card_acceptor = cardacceptor.CardAcceptor()
        card_acceptor.name = 'My Local Bank'
        card_acceptor.city = 'Saint Louis'
        card_acceptor.state = 'MO'
        card_acceptor.postal_code = '63101'
        card_acceptor.country = 'USA'
        transfer_request_mapped.card_acceptor = card_acceptor
    
        transfer_request_mapped.transaction_desc = 'P2P'
        transfer_request_mapped.merchant_id = '123456'

        transfer_ = self._service.get_transfer(transfer_request_mapped)
        assert transfer_.transaction_reference is not None and int(transfer_.transaction_reference) > 0
        assert transfer_.transaction_history.transaction[0] is not None
        assert int(transfer_.transaction_history.transaction[0].response.code) == 00
        assert int(transfer_.transaction_history.transaction[1].response.code) == 00

    def test_payment_request_card(self):
        payment_request_card = paymentrequest.PaymentRequest()
        payment_request_card.local_date = '1226'
        payment_request_card.local_time = '125334'
        payment_request_card.transaction_reference = self.trans_ref_num(19)
        payment_request_card.sender_name = 'John Doe'

        sender_address = senderaddress.SenderAddress()
        sender_address.line1 = '123 Main Street'
        sender_address.line2 = '#5A'
        sender_address.city = 'Arlington'
        sender_address.country_subdivision = 'VA'
        sender_address.postal_code = '22207'
        sender_address.country = 'USA'
        payment_request_card.sender_address = sender_address

        receiving_card = receivingcard.ReceivingCard()
        receiving_card.account_number = '5184680430000014'
        payment_request_card.receiving_card = receiving_card

        receiving_amount = receivingamount.ReceivingAmount()
        receiving_amount.value = '182206'
        receiving_amount.currency = '484'
        payment_request_card.receiving_amount = receiving_amount

        payment_request_card.ica = '009674'
        payment_request_card.processor_id = '9000000442'
        payment_request_card.routing_and_transit_number = '990442082'

        card_acceptor = cardacceptor.CardAcceptor()
        card_acceptor.name = 'My Local Bank'
        card_acceptor.city = 'Saint Louis'
        card_acceptor.state = 'MO'
        card_acceptor.postal_code = '63101'
        card_acceptor.country = 'USA'
        payment_request_card.card_acceptor = card_acceptor

        payment_request_card.transaction_desc = 'P2P'
        payment_request_card.merchant_id = '123456'
        payment_request = self._service.get_transfer(payment_request_card)
        assert payment_request.request_id is not None and int(payment_request.request_id) > 0
        assert payment_request.transaction_history.transaction is not None

    def test_payment_request_mapped(self):
        payment_request_mapped = paymentrequest.PaymentRequest()
        payment_request_mapped.local_date = '1226'
        payment_request_mapped.local_time = '125334'
        payment_request_mapped.transaction_reference = self.trans_ref_num(19)
        payment_request_mapped.sender_name = 'John Doe'

        sender_address = senderaddress.SenderAddress
        sender_address.line1 = '123 Main Street'
        sender_address.line2 = '#5A'
        sender_address.city = 'Arlington'
        sender_address.country_subdivision = 'VA'
        sender_address.postal_code = '22207'
        sender_address.country = 'USA'
        payment_request_mapped.sender_address = sender_address

        receiving_mapped = receivingmapped.ReceivingMapped()
        receiving_mapped.subscriber_id = 'examplePythonReceiving9@email.com'
        receiving_mapped.subscriber_type = 'EMAIL_ADDRESS'
        receiving_mapped.subscriber_alias = 'My Debit Card'
        payment_request_mapped.receiving_mapped = receiving_mapped

        receiving_amount = receivingamount.ReceivingAmount()
        receiving_amount.value = '182206'
        receiving_amount.currency = '484'
        payment_request_mapped.receiving_amount = receiving_amount

        payment_request_mapped.ica = '009674'
        payment_request_mapped.processor_id = '9000000442'
        payment_request_mapped.routing_and_transit_number = '990442082'

        card_acceptor = cardacceptor.CardAcceptor()
        card_acceptor.name = 'My Local Bank'
        card_acceptor.city = 'Saint Louis'
        card_acceptor.state = 'MO'
        card_acceptor.postal_code = '63101'
        card_acceptor.country = 'USA'
        payment_request_mapped.card_acceptor = card_acceptor

        payment_request_mapped.transaction_desc = 'P2P'
        payment_request_mapped.merchant_id = '123456'
        payment_request = self._service.get_transfer(payment_request_mapped)
        assert payment_request.request_id is not None and int(payment_request.request_id) > 0
        assert payment_request.transaction_history.transaction is not None

    def trans_ref_num(self, x, leading_zeroes=True):
        if not leading_zeroes:
            return random.randint(10**(x-1), 10**x-1)
        else:
            if x > 6000:
                return ''.join([str(random.randint(0, 9)) for i in range(x)])
            else:
                return str("%0." + str(x) + "d") % random.randint(0, 10**x-1)