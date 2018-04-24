year = input()
year = int(year)
if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
    print("Bissextile year")
else:
    print("NOT Bissextile year")
