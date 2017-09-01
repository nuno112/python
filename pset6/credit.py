import cs50

def main():
    while(True):
        print("Number: ", end = "")
        cc_number = cs50.get_int()
        if cc_number > 0:
            break
        else:
            print("-.-")
    s = str(cc_number)
    digits = len(s)
    if validate(cc_number):
        if s[0] == "5" and (digits == 13 or digits == 16):
            print("MASTERCARD")
        elif s[0] == "3" and digits == 15:
            print("AMEX")
        elif s[0] == "4" and digits == 16:
            print("VISA")
    else:
        print("INVALID")
    
def validate(n):
    sum1 = 0
    sum2 = 0
    x = 0
    while(n > 0):
        digit = n % 10
        prod1 = 0
        if x % 2 != 0:
            prod1 = digit * 2
            if prod1 // 10 == 0:
                sum1 = sum1 + prod1
            else:
                sum1 = sum1 + prod1 % 10 + 1
        else:
            sum2 = sum2 + digit
        n = n//10
        x = x + 1
    checksum = sum1 + sum2
    if checksum % 10 == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    main()