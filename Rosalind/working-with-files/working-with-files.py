inputFile = open("rosalind_ini5.txt", "r")
outputFile = open("output.txt", "w")
counter = 1

for line in inputFile:
    if (counter % 2 == 0):
        outputFile.write(line)
    counter += 1

inputFile.close()
outputFile.close()
