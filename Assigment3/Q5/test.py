from dataclasses import dataclass
from datetime import datetime
import csv
import Q5_Functions as func
import locale as lc
import sqlite3

lc.setlocale(lc.LC_ALL, 'en_ca')
DATE_FORMAT = '%Y-%m-%d'
DB_FILE = 'Sales_Data.sqlite'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()


def close():
    conn.close()


@dataclass
class Region:
    code:str
    name:str


@dataclass
class Regions:
    regions = []

    def __post_init__(self):
        c.execute('Select * from Region;')
        valid_regions = c.fetchall()
        for region in valid_regions:
            self.regions.append(Region(region[0], region[1]))


    def add_region(self,code,name):
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
        print('Valid Regions: ', end='')
        for region in self.regions:
            print(region.code, end=', ')
    def get_region(self,code):
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
    fileName: str = ''
    region: object = None
    __nameConv = '.csv'

    def get_code(self):
        return self.region.code

    def __post_init__(self):
        self.region = Regions().get_region(self.region)

    def name_conv(self):
        return self.__nameConv

    def validate_file(self):
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
    def __init__(self,sale_id,amount,date,region):
        self.id = sale_id
        self.amount = amount
        try:
            self.date = datetime.strptime(date, DATE_FORMAT).date()
            month = datetime.strptime(date, DATE_FORMAT).month
            self.region = Regions().get_region(region)
            self.quarter = func.get_quarter(int(month))
        except Exception:

            print(self.amount)
            print(self.date)
            print(self.region)
            print(self.quarter)
            print("Daily sales data not added")


    def conv_list(self):
        amount = str(self.amount)
        date = datetime.strftime(self.date, DATE_FORMAT)
        region = self.region
        quarter = str(self.quarter)
        sales_data = [amount,date,region.name,quarter]
        return sales_data

    def from_db(self, date, region):
        query = '''SELECT id FROM sales WHERE salesDate = (?) and region = (?);'''
        try:
            c.execute(query, (date, region,))
            row = c.fetchone()
            return DailySales(row[0], row[1], row[2], row[3])
        except:
            pass



@dataclass
class SalesList:
    dSalesList = []
    badData = False


    def __post_init__(self):
        query = 'SELECT * FROM sales; '
        c.execute(query)
        results = c.fetchall()
        self.dSalesList = []
        for row in results:
            self.dSalesList.append(DailySales(row[0], row[1], row[2], row[3]))


    def addSales(self):
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
        try:
            return self.dSalesList[i]
        except IndexError:
            return None

    def add_sl(self, sales_list):
        for obj in sales_list:
            self.dSalesList.append(obj)

    def list_items(self):
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







def import_file(SALES):
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
                # SALES.append(DailySales( amount, date, region))
            print("File imported successfully.")
    elif test == False:
        print("File could not be imported, check name.")



def view(SALES):
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
            import_file(sales_list)
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

