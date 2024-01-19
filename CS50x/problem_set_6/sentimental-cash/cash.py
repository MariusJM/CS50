quarter = 25
dime = 10
nickel = 5
pennie = 1


while True:
    try:
        amount = float(input("Change:"))
        if amount > 0:
            break
    except:
        print("", end="")
change = amount*100
counter = 0
while change >= quarter:
    change -= quarter
    counter += 1
while change >= dime:
    change -= dime
    counter += 1
while change >= nickel:
    change -= nickel
    counter += 1
while change >= pennie:
    change -= pennie
    counter += 1

print(counter)