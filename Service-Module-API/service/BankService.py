from model.Customer import customer
from repository.CustomerDao import CustomerDAO as cd
from decimal import Decimal

class BankService():

    def fundTransfer(sender_uuid, receiver_uuid, amount):
        amount = Decimal(str(amount))
        sender = cd.find_customer(sender_uuid)
        receiver = cd.find_customer(receiver_uuid)

        senderInitialBlance = sender.balance
        receiverInitialBlance = receiver.balance

        if sender is None or receiver is None:
            raise ValueError("Sender or receiver does not exist")

        if sender.balance < amount or amount < 1:
            raise ValueError("Insufficient balance")

        sender.set_balance(sender.get_balance() - amount)
        receiver.set_balance(receiver.get_balance() + amount)

        if(receiverInitialBlance != receiver.balance or senderInitialBlance != sender.balance ):
            cd.update_customer(sender, receiver)
        
        print("Fund transfer successful")