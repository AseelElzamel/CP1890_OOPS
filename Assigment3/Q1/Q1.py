from dataclasses import dataclass
import csv
import sqlite3
from datetime import datetime


@dataclass
class Customer:  # creates the customer class
    customer_id: int
    fName: str
    lName: str
    companyName: str
    address: str
    city: str
    state: str
    zip: str


def read_csv():  # reads the csv file and handles errors that might occur
    while True:
        try:
            CSVFILE = input('CSV file: ')
            if '.csv' in CSVFILE:

                with open(CSVFILE, newline='') as csvfile:
                    customers = csv.reader(csvfile, delimiter=',')
                    customers = list(customers)
                    customers.pop(0)
                    customer_class_list = []
                    id = 101
                    for i in customers:  # creates each customer object and appends to the list of customers and
                        # returns it
                        customer = Customer(id, i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                        id += 1
                        customer_class_list.append(customer)

                    return customer_class_list

                    break
            else:
                print('Invalid CSV file')
        except ValueError:
            print('Please enter a valid CSV file')
        except FileNotFoundError:
            print("File not found")
        except PermissionError:
            print("Permission denied")
        except Exception:
            print("Something went wrong")


def create_table(database):  # deletes old table and creates new table in the database
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS Customer;')
    c.execute('''CREATE TABLE Customer(
                    customerID  INTEGER PRIMARY KEY     NOT NULL  ,
                    firstName   TEXT                    NOT NULL,
                    lastName    TEXT                    NOT NULL,
                    companyName TEXT                    NULL,
                    address     TEXT                    NULL,
                    city        TEXT                    NULL,
                    state       TEXT                    NULL,
                    zip         TEXT                    NULL
                );''')
    conn.commit()
    conn.close()


def write_to_database(customer_class_list, database):  # inserts the customer list information into the database table.
    conn = sqlite3.connect(database)
    c = conn.cursor()
    query = 'INSERT INTO Customer VALUES (?,?,?,?,?,?,?,?);'
    for customer in customer_class_list:
        c.execute(query, (
        customer.customer_id, customer.fName, customer.lName, customer.companyName, customer.address, customer.city,
        customer.state, customer.zip))
    conn.commit()
    conn.close()
    print('Database successfully created')


def validate_db():  # validates the database input
    while True:
        db_file = input('DB file: ')
        if '.sqlite' not in db_file:
            print('Invalid DB file')
        else:
            return db_file
            break


def main():  # program body
    print('Customer Data Importer')
    print()
    customer_list = read_csv()

    DB_FILE = validate_db()
    print('Table name: Customer')
    print()

    database = DB_FILE
    create_table(database)
    print('All old rows deleted from Customer table')

    write_to_database(customer_list, database)
    print(f' {len(customer_list)} rows(s) inserted into Customer table')


if __name__ == '__main__':
    main()
