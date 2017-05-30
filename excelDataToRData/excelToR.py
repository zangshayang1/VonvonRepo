import sys
import os


###################################################################################
# This script is to convert multiple csv files into one "R-operatible" dataframe.
# Each bp in an input file can be viewed as an x-coordinate on x-axis.
# It corresponds to mutiple field values, which can be viewed as multiple y-coordinates.
# We want to create an output dataframe such that the first column is bp,
#   the second is one field value, the third column is the corresponding field name.
##################################################################################

"""
@ Input: filename
@ Output: List<Ruple>

Note: the input file is generated in Windows env, so the newline character is '\r\n'
"""
def excelFileToRDataList(filename):
    f = open(filename, 'r')
    header = f.readline().rstrip('\r\n').split(',')
    rowlength = len(header)
    print header

    RDataList = []
    for line in f:
        linelist = line.rstrip('\r\n').split(',')
        bp = linelist[0]
        for colidx in range(1, rowlength):
            RDataList.append(Ruple(bp, linelist[colidx], header[colidx]))
    f.close()
    RDataList.sort(key = lambda ruple : ruple.field)
    return RDataList


"""
This defines a data access object
"""
class Ruple():
    def __init__(self, basepair, val, field):
        self.basepair = basepair
        self.val = val
        self.field = field

"""
main() includes:
1. open outputfile, write header.
2. traverse input directory, convert each file into a list of Ruples.
3. write each such list to the output.
"""
def main():

    outputname = sys.argv[1]
    output = open(outputname, 'w')
    output.write("bp, value, field\n")

    rootdir = sys.argv[2]
    for root, dirlist, filelist in os.walk(rootdir):
        for f in filelist:
            RDataList = excelFileToRDataList(rootdir + f)
            WriteDataList = []
            for ruple in RDataList:
                WriteDataList.append(ruple.basepair + "," + ruple.val + "," + ruple.field)
            output.write('\n'.join(WriteDataList)) # join operation only weave together all the string in WriteDataList by '\n', lacking a '\n' in the end.
            output.write('\n')
    output.close()


if __name__ == '__main__':
    main()
