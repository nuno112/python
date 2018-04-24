from OrderedDictionary import *

fruits = OrderedDictionary()
print(fruits)

fruits["pomme"] = 52
fruits["poire"] = 34
fruits["prune"] = 128
fruits["melon"] = 15
print(fruits)

fruits.sort()
print(fruits)

legumes = OrderedDictionary(carrot=26, pear=20)
print(legumes)

print(len(legumes))

legumes.reverse()
print(legumes)

fruits = fruits + legumes
print(fruits)

del fruits["pear"]
print("pear" in fruits)

print(legumes["pear"])

for key in legumes:
    print(key)

print(legumes.keys())
print(legumes.values())

for x, qt in legumes.items():
    print("{0} ({1})".format(x, qt))
