import cs50

def main():
    print("Height: ", end = "")
    
    while(True):
        height = cs50.get_int()
        if height < 23 and height > 0:
            break
    
    for i in range(height + 1):
        build(height - i, " ")
        build(i, "#")
        print("  ", end = "")
        build(i, "#")
        print()
        
def build(n, s):
    for i in range(n):
        print(s, end = "")
        
if __name__ == "__main__":
    main()