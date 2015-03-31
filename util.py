import math
import sys


def entropy(byteArr):
    fileSize = len(byteArr)
    print 'File size in bytes:'
    print fileSize
    print

    # calculate the frequency of each byte value in the file
    freqList = []
    for b in range(256):
        ctr = 0
        for byte in byteArr:
            if byte == b:
                ctr += 1
        freqList.append(float(ctr) / fileSize)
    # print 'Frequencies of each byte-character:'
    # print freqList
    # print

    # Shannon entropy
    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    ent = -ent
    print 'Shannon entropy (min bits per byte-character):'
    print ent
    print
    print 'Min possible file size assuming max theoretical compression efficiency:'
    print (ent * fileSize), 'in bits'
    print (ent * fileSize) / 8, 'in bytes'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: file_entropy.py [path]filename"
        sys.exit()
    with open(sys.argv[1], "rb") as f:
        entropy(map(ord, f.read()))
