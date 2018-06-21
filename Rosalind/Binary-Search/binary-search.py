# Given a sorted array and a list of integers, output the index of each integer
# in the array. If the integer is not in the array, print -1

from math import floor


def binarySearch(arr, item, low=0, high=None):
    if high is None:
        high = len(arr)
    mid = low + (high-low) // 2
    if high - low + 1 <= 0 or mid == high:
        return -1
    else:
        guess = arr[mid]
        if guess == item:
            return mid + 1
        if item < guess:
            return binarySearch(arr, item, low, mid)
        else:
            return binarySearch(arr, item, (mid+1), high)


output = []
sortedArray = []
integerList = []

f = open("rosalind_bins.txt", "r")
data = f.readlines()
f.close()
sortedArrayString = data[2].split(" ")
integerListString = data[3].split(" ")


for elem in sortedArrayString:
    sortedArray.append(int(elem))
for elem in integerListString:
    integerList.append(int(elem))

for n in integerList:
    output.append(binarySearch(sortedArray, n))

f2 = open("output.txt", "w")
for n in output:
    f2.write(str(n) + " ")
