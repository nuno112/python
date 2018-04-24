from random import randrange


def troll(trollNumber):
    """Takes in a number and changes the decorated
    function first paramenter to a random word in the list"""

    def decorator(function):
        """This is the decorator. It is the one that calls the moddified
        function"""

        def moddedFunction(*args, **kwargs):
            """The moddified function returned to the decorator. It changes
            the first parameter passed to the original function to a word
            in trollList"""

            trollList = ["Bazinga", "Batman", "Kappa", "Brah", "Mah Dude",
                         "Memester", "Potato"]
            return function(trollList[trollNumber])
        return moddedFunction
    return decorator


def fuckify(function):
    """Takes in a number and does some shenanigans to the decorated function"""
    def moddedFunction(*args, **kwargs):
        """The moddified function returned to the decorator. I puts a
        modern spin to the trolling level"""

        print("\n\nYeah... You like that, you fucking retard?")
        print("Are you fucking sorry??\n\n")
        return function()
    return moddedFunction


@fuckify
@troll(randrange(6))
def sayHi(s):
    print("Hello, " + s + "!")


@troll(randrange(6))
def favoriteColor(c):
    print("My fav color is: " + c)


name = input("Name pls: ")
color = input("Favorite color pls: ")
sayHi(name)
favoriteColor(color)
