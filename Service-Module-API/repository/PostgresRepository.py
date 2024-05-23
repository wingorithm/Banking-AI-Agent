import psycopg2
import random
from decimal import Decimal
from model.Customer import customer

class postgresRepository():
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="mytest",
            user="postgres",
            password="psqladmin",
            host="localhost",
            port="9096"
        )

        self.cur = self.conn.cursor()
    
    def find_user_byUUID(self, uuid):
        print(uuid)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE uuid = %s;", (uuid,))
        customer = cur.fetchone()
        cur.close()
        return  customer

    @staticmethod
    def generate_uuid():
        return "BLU" + str(random.randint(1000000000, 9999999999))

    @staticmethod
    def generate_cin():
        return random.randint(100000000, 999999999)
    
    def create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
            cin INTEGER PRIMARY KEY,
            uuid VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            account CHAR(12) NOT NULL,
            balance DECIMAL(12, 2) NOT NULL
        );
        """
        self.cur.execute(create_table_sql)
        self.conn.commit()
    
    
    def insert_data(self):
        for _ in range(5): 
            uuid = "BLU" + str(random.randint(1000000000, 9999999999))
            name = "User" + str(_ + 1)
            account = "008" + str(random.randint(100000000, 999999999))
            balance = round(random.uniform(10000000, 1000000000), 2)
            
            self.cur.execute("""
                INSERT INTO users (cin, uuid, name, account, balance) 
                VALUES (%s, %s, %s, %s, %s)
            """, (random.randint(100000000, 999999999), uuid, name, account, balance))

            self.conn.commit()

    def save(self, customer : customer):
        self.cur.execute("""
            INSERT INTO users (cin, uuid, name, account, balance) 
            VALUES (%s, %s, %s, %s, %s)
        """, (customer.cin, customer.uuid, customer.name, customer.account, customer.balance))
        self.conn.commit()
    
    def update_customer(self, data : customer):  
        self.cur.execute("""
                        UPDATE users 
                        SET name = %s, account = %s, balance = %s
                        WHERE uuid = %s
                        """, (data.name, data.account, data.balance, data.uuid))
        self.conn.commit()