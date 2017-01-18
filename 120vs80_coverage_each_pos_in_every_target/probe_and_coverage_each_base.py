##this is to link 


import sys
input1 = open(sys.argv[1], "r")
input2 = open(sys.argv[2], "r")
output = open(sys.argv[3], "w")

##title
output.write('Chrom' + '\t' + 'Pos' +'\t' + 'Depth' +'\t' + 'Pos_normalized' +'\t'+'Probe_coverage'+'\t'+'Target'+'\n')

##collasped.tsv this is the collapsed_coverage for each position in target
dict = {}
for line in input1:
    x = line.strip().split('\t')
    key = x[0] + '\t' + x[1]
    if key not in dict:
        dict[key] = x[2]

##probe_target_pos.txt this is the output after bedtools coverage -d and normalized.py
Target = 1.0
for line in input2:
    y = line.strip().split('\t')
    key = y[0] + '\t' + y[1]
    if key in dict:
        if float(y[2]) <1.0:
            output.write(y[0]+'\t'+y[1]+'\t'+dict[key]+'\t'+y[2] +'\t'+y[3]+'\t'+str(Target)+'\n')
        else:
            output.write(y[0]+'\t'+y[1]+'\t'+dict[key]+'\t'+y[2]+'\t'+y[3]+'\t'+str(Target)+'\n')
            Target+=1


input1.close()
input2.close()
output.close()



