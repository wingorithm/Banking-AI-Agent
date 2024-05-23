from repository.PostgresRepository import postgresRepository
from repository.CustomerDao import CustomerDAO as cd
from service.BankService import BankService as bankService

ps = postgresRepository()

# ps.create_table()
# ps.insert_data()
# result = cd.find_customer("BLU2344216434")
# print("balance", result.balance)


try:
    bankService.fundTransfer('BLU5354987807', 'BLU2344216434', 7777.00)
except Exception as e:
    print(e)