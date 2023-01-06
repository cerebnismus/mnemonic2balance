import sys
import getopt
import random

input = open('wordlist.txt', 'r').readlines()
output = open('12words.txt', 'w')


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def GenerateWordLines(prefix=False, number=20):

    while number > 0:
        if prefix == 'TRUE':
            print("Not Supported.")
        elif prefix:
            word1 = prefix
        else:
            word1 = input[int(random.uniform(0, len(input)))]
            word2 = input[int(random.uniform(0, len(input)))]
            word3 = input[int(random.uniform(0, len(input)))]
            word4 = input[int(random.uniform(0, len(input)))]
            word5 = input[int(random.uniform(0, len(input)))]
            word6 = input[int(random.uniform(0, len(input)))]
            word7 = input[int(random.uniform(0, len(input)))]
            word8 = input[int(random.uniform(0, len(input)))]
            word9 = input[int(random.uniform(0, len(input)))]
            word10 = input[int(random.uniform(0, len(input)))]
            word11 = input[int(random.uniform(0, len(input)))]
            word12 = input[int(random.uniform(0, len(input)))]

            output.write(" %s %s %s %s %s %s %s %s %s %s %s %s " % (
            word1.rstrip(), word2.rstrip(), word3.rstrip(), word4.rstrip(), word5.rstrip(), word6.rstrip(),
            word7.rstrip(),word8.rstrip(), word9.rstrip(), word10.rstrip(), word11.rstrip(), word12.rstrip()))
            output.write("\n")


        print(output, " %s %s %s %s %s %s %s %s %s %s %s %s " % (
        word1.rstrip(), word2.rstrip(), word3.rstrip(), word4.rstrip(), word5.rstrip(), word6.rstrip(), word7.rstrip(),
        word8.rstrip(), word9.rstrip(), word10.rstrip(), word11.rstrip(), word12.rstrip()))

        number -= 1


def main(argv=None):
    numberOfLines = 20
    prefix = False

    GenerateWordLines(prefix, numberOfLines)

if __name__ == "__main__":
    sys.exit(main())