from dataclasses import dataclass
from datetime import datetime
import csv
import Q5_Functions as func
import locale as lc
import sqlite3
#Import proper modules for function in the program


lc.setlocale(lc.LC_ALL, 'en_ca')
DATE_FORMAT = '%Y-%m-%d'
DB_FILE = 'Sales_Data.sqlite'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
#Set locale, date format, Database file name, and opens connection


def close():
    conn.close()


@dataclass
class Region:
    """
    Class to represent a region code, and the name related
    """
    code:str
    name:str


@dataclass
class Regions:
    #Instantiates with an empty list attribute
    regions = []

    def __post_init__(self):
        #Post intializing reads available regions from the database and appends it to the list
        c.execute('Select * from Region;')
        valid_regions = c.fetchall()
        for region in valid_regions:
            self.regions.append(Region(region[0], region[1]))


    def add_region(self,code,name):
        #adds a region object to the regions list and to the database
        new_region = Region(code, name.title())

        region_codes = []
        for region in self.regions:
            region_codes.append(region.code)
        if new_region.code in region_codes:
            pass
        else:
            self.regions.append(new_region)
            c.execute('''insert into Region values (?,?);''', (new_region.code, new_region.name,))
            conn.commit()

    def valid_regions(self):
        #prints the valid region codes for data entry
        print('Valid Regions: ', end='')
        for region in self.regions:
            print(region.code, end=', ')

    def get_region(self,code):
        #gets a region by the provided region code
        num = 0
        for region in self.regions:
            if region.code == code:
                break
            else:
                num +=1
                if num == len(self.regions)-1:
                    return 'Invalid Region'
                    break
        return self.regions[num]

@dataclass
class File:
    #Class for storing a file
    fileName: str = ''
    region: object = None
    __nameConv = '.csv'

    def get_code(self):
        #gets region code of the region object
        return self.region.code

    def __post_init__(self):
        #post initializing gets a region for the region object attribute
        self.region = Regions().get_region(self.region)

    def name_conv(self):
        #returns naming convention
        return self.__nameConv

    def validate_file(self):
        #Validates the file to make sure it exists and if it has already been added to the DB
        try:
            with open(f"{self.fileName}{self.__nameConv}") as csvfile:
                sales_data = csv.reader(csvfile)

                c.execute('insert into ImportedFiles values(?);',(f'{self.fileName}{self.__nameConv}',))
                conn.commit()
            return True
        except FileNotFoundError:
            return False
        except sqlite3.IntegrityError:
            print("File already imported")
            return False


@dataclass
class DailySales:
    #Daily sales class used for storing proper data for a daily sales record
    def __init__(self,sale_id,amount,date,region):
        self.id = sale_id
        self.amount = amount
        try:
            #tries to convert received attributes into proper data format
            self.date = datetime.strptime(date, DATE_FORMAT).date()
            month = datetime.strptime(date, DATE_FORMAT).month
            self.region = Regions().get_region(region)
            self.quarter = func.get_quarter(int(month))
        except Exception:
            #Prompts user upon error
            print("Daily sales data not added")


    def conv_list(self):
        #Converts data to list for CSV file (not used in DB iteration of program)
        amount = str(self.amount)
        date = datetime.strftime(self.date, DATE_FORMAT)
        region = self.region
        quarter = str(self.quarter)
        sales_data = [amount,date,region.name,quarter]
        return sales_data

    def from_db(self, date, region):
        #Returns a DailySales object based on a date and region parameter
        query = '''SELECT id FROM sales WHERE salesDate = (?) and region = (?);'''
        try:
            c.execute(query, (date, region,))
            row = c.fetchone()
            return DailySales(row[0], row[1], row[2], row[3])
        except:
            pass



@dataclass
class SalesList:
    #Intstantiates with a empty list attribute and attribute to signify badData
    dSalesList = []
    badData = False


    def __post_init__(self):
        #Post initializing reads the salesData from the DB into the sales list as Daily Sales objects
        query = 'SELECT * FROM sales; '
        c.execute(query)
        results = c.fetchall()
        self.dSalesList = []
        for row in results:
            self.dSalesList.append(DailySales(row[0], row[1], row[2], row[3]))


    def addSales(self):
        #Adds sales data to the DB after proper validation
        while True:
            try:
                amount = float(input("Enter sales amount: "))
                break
            except ValueError:
                print("Sales amount must be a float, please try again.")
                print()
                self.badData = True
                continue
        while True:
            try:
                date = datetime.strptime(input("Enter date (YYYY-MM-DD): "), DATE_FORMAT).date()
                if date.year > 1900 and date.year < 2501:
                    break
                else:
                    print("Year must be between 1900 and 2501")
                    raise ValueError
            except ValueError:
                print("Invalid date format, please try again.")
                print()
                self.badData = True
                continue
        while True:
            code = str(input("Enter region: "))
            valid_codes = []
            regions = Regions().regions
            for region in regions:
                valid_codes.append(region.code)

            if code in valid_codes:
                c.execute('insert into Sales(amount,salesDate,region) values(?,?,?);',(amount,date,code))
                conn.commit()
                print("Sales added successfully.")
                break

            else:
                print("Invalid region, ")
                Regions().valid_regions()
                print()


        self.badData = False



    def retr_fr_index(self, i):
        #Retrieves an object from the sales list by the index
        try:
            return self.dSalesList[i]
        except IndexError:
            return None

    def add_sl(self, sales_list):
        #Adds a SalesList object to the current sales list
        for obj in sales_list:
            self.dSalesList.append(obj)

    def list_items(self):
        #returns the amount of object in the list
        return len(self.dSalesList)


def display_title():
    print('SALES DATA IMPORTER')
    print()


def display_menu():
    print('COMMAND MENU' +
          '\nview - View all sales' +
          '\nadd - Add sales' +
          '\nimport - Import sales from file' +
          '\nmenu - Show menu' +
          '\nexit - Exit program')
    print()







def import_file():
    #Imports validated csv file and after proper validation, and inserts the data into the DB
    file = input("Enter file name: ")
    file_obj = File(file)
    test = file_obj.validate_file()
    if test == True:
        with open(f"{file}{file_obj.name_conv()}") as sales:
            sale = csv.reader(sales)
            for item in sale:
                id = item[0]
                amount = item[1]
                date = item[2]
                region = item[3]
                query = '''INSERT INTO Sales (amount, salesDate, region) Values (?, ?, ?)'''
                c.execute(query, (amount, date, region))
                conn.commit()
            print("File imported successfully.")
    elif test == False:
        print("File could not be imported, check name.")



def view(SALES):
    #Displays a formatted view of the SalesData from the DB
    if len(SALES) == 0:
        print('No Sales to view! Import first!')
        print()
    else:
        print('\tDate\t\t\t\tQuarter\t\t\tRegion\t\t\tAmount')
        print('=' * 66)

        for i, obj in enumerate(SALES,start=1):
            print('{}\t{}\t\t\t\t{}\t\t\t{:<10}{:>16}'.format(i, obj.date, obj.quarter, obj.region.name,
                                                               lc.currency(obj.amount, grouping=True)))
        print('=' * 66)
        total = []
        for obj in SALES:
            total.append(obj.amount)
        total_value = sum(total)
        total_value = lc.currency(total_value, grouping=True)
        print('TOTAL:{:>60}'.format(total_value))
        print()

def main():
    #Main function putting each piece in collaboration to run the program in proper fashion
    display_title()
    display_menu()

    while True:
        SALES = SalesList()
        sales_list = SALES.dSalesList
        print()
        cmd = input('Please enter a command: ').lower()
        print()
        if cmd == 'view':
            view(sales_list)
        elif cmd == 'add':
            SALES.addSales()
        elif cmd == 'import':
            import_file()
        elif cmd == 'menu':
            display_menu()
        elif cmd == 'exit':
            print()
            print('Bye!')
            break
        else:
            print('Please enter a valid command')

if __name__ == '__main__':
    main()
