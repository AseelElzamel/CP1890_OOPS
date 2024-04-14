from dataclasses import dataclass
from datetime import datetime
import locale
import csv
import sales_importer_functions as psi


@dataclass
class Region:
    code:str = ''
    name:str = ''

@dataclass
class Regions:
    regions:list = None

    def r_by_code(self, code):
        for region in self.regions:
            if region.code == code:
                return region
            else:
                print("Region not found")

    def valid_codes(self):
        counter = 0
        print("List of valid codes:")
        for region in self.regions:
            counter = counter + 1
            print(f"{counter}. {region.code}")





@dataclass
class File:
    fileName:str=''
    region:object = None
    name_conv:str = '.csv'

    def code_fr_file(self):
        file = f"{self.fileName}{self.name_conv}"
        with open(file) as sales:
            s_data = csv.reader(sales)
            for row in s_data:
                if row[2] == 'West'
                    return

    def file_check(self):
        if self.fileName.endswith('.csv'):
            return True
        else:
            return False





@dataclass
class DailySales:
    amount:str
    date:str
    region:str
    quarter:str

    def conv_list(self):
        ammount = str(self.amount)
        date = datetime.strftime(self.date, '%Y-%m-%d')
        region = str(self.region.code)
        quarter = str(self.quarter)
        sales_data = [ammount,date,region,quarter]
        return sales_data

    def __post_init__(self):
        self.amount = float(self.amount)
        self.date = datetime(self.date)
        self.region = Region(self.region)
        self.quarter = int(self.quarter)

@dataclass
class SalesList:
    sales_data:list = []


def import_file(salesList, fileName):
    with open(fileName) as sales:
        sale = csv.reader(sales)
        for data in sale:
            salesList.