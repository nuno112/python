from random import randrange


def getBet():
    try:
        x = input("Choose amount to bet ")
        x = float(x)
        if x < 0 or x > money:
            raise ValueError()
        return x
    except ValueError:
        print("input correct number")


def getNumber():
    try:
        x = input("Choose a number between 0 and 49 ")
        x = int(x)
        if x < 0 or x > 49:
            raise ValueError()
        return x
    except ValueError:
        print("input correct number")


def checkResult(a, b):
    if a == b:
        return "win"
    elif (a % 2 == 0 and b % 2 == 0) or (a % 2 != 0 and b % 2 != 0):
        return "semiwin"
    else:
        return "loss"


def updateMoney(result):
    global money
    global bet
    if result == "win":
        money = money + bet * 3
    elif result == "semiwin":
        money = money + bet * 0.5
    else:
        money = money - bet


if __name__ == "__main__":
    money = 50.0
    while True:
        if money <= 0:
            print("Game Over, no money left")
            break
        bet = getBet()
        if bet is not None:
            playerNum = getNumber()
            if playerNum is not None:
                casinoNum = randrange(50)
                result = checkResult(playerNum, casinoNum)
                updateMoney(result)
                print("Result: " + result + ". Money: " + str(money))
