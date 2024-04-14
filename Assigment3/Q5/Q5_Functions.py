def get_quarter(data):
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
    return quarter