import sys

def normalize (file):
	#this is to get pos_nomalized_probe
	ls = []
	target=1
	base=1
	for line in file:
		element=line.rstrip().split("\t")
		length= 240
		#pos = int( element[1]) + int(base)
		if base <= 120:
			pos=int( element[1]) + int(base)
			pos_normalized = float(int(base))/length
			ls.append([element[0], str(pos),str(pos_normalized),element[4],str(target)])
			base += 1 
		##below is for the second probe 
		elif base > 120 and base < 240:
			pos=int( element[1]) + int(base)-120
			pos_normalized = float(int(base))/length
			ls.append([element[0], str(pos),str(pos_normalized),element[4],str(target)])
			base += 1

		elif base == 240:
			pos=int( element[1]) + int(base)-120
			pos_normalized = float(int(base))/length
			ls.append([element[0], str(pos),str(pos_normalized),element[4],str(target)])
			target += 1
			base=1
	return ls


def match_line(file, input_ls):
 	#this to match probe_normalized_pos with I4_120
 	output_ls = []
 	dict={}
 	for line in file:
		x = line.rstrip().split('\t')
		key = x[0], x[1]
		if key not in dict:
			dict[key]=x[2]
	for element in input_ls:
		key = element[0], element[1]
		if key in dict:
			output_ls.append([element[0], element[1], element[2], dict[key], element[4]])
	print output_ls
	return output_ls
	#chr, pos, nor_pos, depth, target
	

def match_GC(file, input_ls):
	#this is to assign the GC to the target 
	output_ls = []
	dict = {}
	for line in file:
		x = line.strip().split('\t')
		key = x[0]+'\t'+x[1]

		if key not in dict:
			dict [key] = x[9]

	for element in input_ls:
		key = element[0]+'\t'+str(int(element[1])-1)
		if key in dict:
			GC=dict[key]
			output_ls.append(element[0]+'\t'+element[1]+'\t'+element[2]+'\t'+element[3]+'\t'+element[4]+'\t'+GC+'\n')
		else:
			output_ls.append(element[0]+'\t'+element[1]+'\t'+element[2]+'\t'+element[3]+'\t'+element[4]+'\t'+GC+'\n')
	return output_ls



def write(ls):
	output = open(sys.argv[4], "w")
	output.write("Chrom"+'\t'+"Pos"+'\t'+"Normalized_pos"+'\t'+"Depth"+'\t'+"Target"+'\t'+"X.gc"+'\n')
	for element in ls:
		output.write(element)
	output.close()
	return None



###main function
input1=open(sys.argv[1], "r") ##one_probe_of_each_target_120_each_base
input2=open(sys.argv[2], "r") ###I4_20 (coverage of each pos)
input3=open(sys.argv[3], "r") ###Target_with_one_120(provide GC)
output=open(sys.argv[4], "w")

normalized = normalize(input1)
print len(normalized)
output_ls = match_line(input2, normalized)
print len(output_ls)
matched_GC_ls = match_GC(input3, output_ls)
write(matched_GC_ls)

input1.close()
input2.close()
input3.close()
output.close()




