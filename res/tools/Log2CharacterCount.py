import sys

if __name__ == "__main__":
    f = open(sys.argv[1])
    text = f.read()
    f.close()
    text_length = len(text)
    print("Character Count: " + str(text_length) + ", Estimated Word Count: " + str(text_length / 2))