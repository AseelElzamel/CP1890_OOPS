# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:39:03 2023

@author: Michael.Agonsi
"""


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


def region():
    region = {'w': 'West',
              'm': 'Mountain',
              'c': 'Central',
              'e': 'East'}
    return region


def get_amount():
    while True:

        amount = float(input('Amount:\t\t\t'))
        if amount >= 0:
            return amount
            break
        else:
            print('Please enter a valid amount')
            print()


def get_year():
    while True:
        year = int(input('Year:\t\t\t'))
        if year > 1900 and year < 2501:
            return year
            break
        else:
            print('Please enter a year between 1900 and 2500!')
            print()


def get_month(data):
    while True:
        month = data

        if month >= 1 and month <= 3:
            quarter = 1
            break
        elif month >= 4 and month <= 6:
            quarter = 2
            break
        elif month >= 7 and month <= 9:
            quarter = 3
            break
        elif month >= 10 and month <= 12:
            quarter = 4
            break
        else:
            print('Please enter a valid data!')
            print()
    return month, quarter


def get_date():
    month, quarter = get_month()
    while True:
        day = int(input('Day (01-31):\t\t'))

        if day > 0 and month == 2:
            return month, quarter, day
            break
        elif (day > 0 and day <= 30) and (month == 9 or month == 4 or month == 6 or month == 11):
            return month, quarter, day
            break
        elif (day > 0 and day <= 30 and day <= 31) and (
                month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            return month, quarter, day
            break
        else:
            print('Please enter a valid data')
            print()


def get_region():
    regions = region()
    for reg in regions.values():
        print(reg, end=', ')
    print()
    while True:
        Region = input('Enter w, m,c or e: ').lower()
        if Region in regions.keys():
            return Region
            break
        else:
            print('Not a valid entry!')


def write(SALES):
    import csv
    Sales = []
    for sale in SALES:
        Sales.append(sale.values())
    with open('sales.csv', 'w', newline='') as sales:
        data = csv.writer(sales)
        data.writerows(Sales)


def import_file(SALES):
    import csv
    with open('sales.csv') as sales:
        sale = csv.reader(sales)
        for data in sale:
            sale_data = {'year': data[0],
                         'month': data[1],
                         'day': data[2],
                         'quarter': data[3],
                         'region': data[4],
                         'amount': data[5]}
            SALES.append(sale_data)


def view(SALES):
    if len(SALES) == 0:
        print('No Sales to view! Import first!')
        print()
    else:
        reg = region()
        print('\tDate\t\t\t\tQuarter\t\t\tRegion\t\t\tAmount')
        print('=' * 65)
        i = 1
        for sale in SALES:
            print('{}   {}-{}-{}\t\t\t\t{}\t\t\t{}{}${:,.2f}'.format(i, sale['year'], sale['month'], sale['day'],
                                                                     sale['quarter'], reg[sale['region']],
                                                                     " " * (14 - len(reg[sale['region']])),
                                                                     float(sale['amount'])))
            i += 1
        print('=' * 65)
        total = []
        for sale in SALES:
            total.append(float(sale['amount']))
        total_value = sum(total)
        print('TOTAL:\t\t\t\t\t\t\t\t\t\t\t\t${:,.2f}'.format(total_value))
        print()


def add(SALES):
    amount = get_amount()
    year = get_year()
    month, quarter, day = get_date()
    region = get_region()

    sale = {'year': year,
            'month': month,
            'day': day,
            'quarter': quarter,
            'region': region,
            'amount': amount}

    SALES.append(sale)

    write(SALES)
    print('Sales Data has been added.')


def main():
    display_title()
    display_menu()
    SALES = []
    while True:
        print()
        cmd = input('Please enter a command: ').lower()
        print()
        if cmd == 'view':
            view(SALES)
        elif cmd == 'add':
            add(SALES)
        elif cmd == 'import':
            import_file(SALES)
            print('Sales Data has be imported from files successfully')
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



