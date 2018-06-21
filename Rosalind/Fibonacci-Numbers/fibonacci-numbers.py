# Given an integer 0>n<=25, calculate the corresponding nth Fibonacci number

# a = F(n-2)
# b = F(n-1)
# c = F(n)

GIVEN_NUMBER = 23

a = 0
b = 1
c = 1

for i in range(1, GIVEN_NUMBER):
    c = a + b
    a = b
    b = c

print(c)
