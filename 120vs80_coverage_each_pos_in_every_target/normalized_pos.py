##this is to normalize the pos in each target (0-1); 
##the input is the out put of "bedtools coverage -d -a probe.bed -b manifest.bed"
##NOTE: the starting position in manifest has been -1 to fit the later python code

import sys
input = open (sys.argv[1], "r")
output = open (sys.argv[2], "w")

output.write('Chrom'+'\t'+'Pos'+'\t'+'Pos_normalized'+'\t'+'Probe_coverage'+'\n')

for line in input:
    element = line.strip().split("\t")
    length= float( element[2]) - int( element[1])
    pos_normalized = float( int( element[3])/ length)
    pos = int( element[1]) + int(element[3])
    output.write(element[0] + '\t' + str(pos) + '\t' + str(pos_normalized) + '\t' +element[4] + '\n')

input.close()
output.close()
