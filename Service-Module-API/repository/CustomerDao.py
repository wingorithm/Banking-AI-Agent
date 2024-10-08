import psycopg2
from repository.PostgresRepository import postgresRepository
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from model.Customer import customer 

ps = postgresRepository()

# DB (X)
# REPO -> ORM
# DAO -> find, update, delete 
# DTO (oper antar service)

class CustomerDAO:
    def find_customer(uuid : str):
        try:
            customer_data = ps.find_user_byUUID(uuid)
            if customer_data is None:
                raise ValueError("Customer not found")
            
            return customer(*customer_data)

        except (OperationalError, InterfaceError) as e:
            print(f"Database connection error: {e}")
        
        except DatabaseError as e:
            print(f"Database error: {e}")
        
        except ValueError as e:
            print(f"Error: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def find_customer_byAcc(acc : str):
        try:
            customer_data = ps.find_user_byAcc(acc)
            if customer_data is None:
                raise ValueError("Customer not found")
            
            return customer(*customer_data)

        except (OperationalError, InterfaceError) as e:
            print(f"Database connection error: {e}")
        
        except DatabaseError as e:
            print(f"Database error: {e}")
        
        except ValueError as e:
            print(f"Error: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_customer(sender: customer, receiver: customer):
        ps.update_customer(sender)
        ps.update_customer(receiver)
        