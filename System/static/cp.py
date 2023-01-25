import os


if __name__ == "__main__":
    f = open('file.txt', 'r')
    for line in f.readlines():
        os.system("cp {} .".format(line[:-1]))