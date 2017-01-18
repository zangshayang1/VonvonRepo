import sys
input = open (sys.argv[1], "r")
output = open (sys.argv[2], "w")

output.write('Chrom'+'\t'+'Pos'+'\t'+'Pos_normalized'+'\n')


for line in input:
	count =1
	x = line.rstrip().split('\t')
	fake_start = int(x[1]) - 1  
	end = x[2]
	pos = fake_start +count
	length = float(x[3])+1
	while pos <= int(end):
		nol_pos = count / length
		output.write(x[0]+'\t'+str(pos)+'\t'+str(nol_pos)+'\n')
		pos +=1
		count +=1


input.close()
output.close()


