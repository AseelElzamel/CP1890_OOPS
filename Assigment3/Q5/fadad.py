from dataclasses import dataclass
from datetime import datetime
import csv
import Q5_Functions as func
DATE_FORMAT = '%Y-%m-%d'
@dataclass
class Region:
    code:str
    name:str


@dataclass
class Regions:
    regions = []

    def __post_init__(self):
        valid_regions = {'e':'East','w':'West','m':'Mountain','c':'Central'}
        for code,name in valid_regions.items():
            self.regions.append(Region(code,name))
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
    fileName:str
    region:str
    __nameConv ='.csv'

    def get_code(self):
        return self.region.code

    def __post_init__(self):
        self.region = Regions().get_region(self.region)

    def validate_file(self):
        try:
            with open(f"{self.fileName}{self.__nameConv}") as csvfile:
                sales_data = csv.reader(csvfile)
            return f"{self.fileName}{self.__nameConv}"
        except FileNotFoundError:
            return 'Invalid file name'




@dataclass
class DailySales:
    def __init__(self,amount,date,region):
        try:
            month = datetime.strptime(date, DATE_FORMAT).month
            self.amount = float(amount)
            self.date = datetime.strptime(date, DATE_FORMAT).date()
            self.region = Regions().get_region(region)
            self.quarter = func.get_quarter(int(month))
        except Exception:
            return 'Invalid'


    def conv_list(self):
        amount = str(self.amount)
        date = datetime.strftime(self.date, DATE_FORMAT)
        region = self.region
        quarter = str(self.quarter)
        sales_data = [amount,date,region.name,quarter]
        return sales_data


@dataclass
class SalesList:
    dSalesList: list= None
    badData: bool= False

    def addSales(self):
        amount = float(input("Enter sales amount: "))
        date = datetime.strptime(input("Enter date (YYYY-MM-DD): "),DATE_FORMAT)
        region = str(input("Enter region: "))
        # if region.lower() == 'west'
        # dailysales = DailySales(amount,date,region)






dailysales = DailySales('2000','2003-05-02','e')
#
# region = Regions()
#
# file = File('test.csv','e')
# print(file.get_code())

print(dailysales.conv_list())