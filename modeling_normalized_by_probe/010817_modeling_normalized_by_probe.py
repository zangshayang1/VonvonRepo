import sys

def normalize (file):
	#this is to get pos_nomalized_probe
	ls = []
	target=1
	for line in file:
		element=line.split("\t")
		length= float( element[2]) - int( element[1])
		pos_normalized = float( int( element[3])/ length)
		pos = int( element[1]) + int(element[3])
		if pos_normalized ==1:
			ls.append([element[0], str(pos),str(pos_normalized),element[4],str(target)])
			target += 1 
		else:
			ls.append([element[0], str(pos),str(pos_normalized),element[4],str(target)])
	return ls

def match_line(file, input_ls):
 	#this to match probe_normalized_pos with I4_120
 	output_ls = []
 	dict={}
 	for line in file:
		x = line.strip().split('\t')
		key = x[0]+'\t'+x[1]
		if key not in dict:
			dict[key]=x[2]
	for element in input_ls:
		key = element[0]+'\t'+element[1]
		if key in dict:
			output_ls.append(key+'\t'+x[2]+'\t'+dict[key]+'\t'+x[4]+'\n')
	return output_ls

def write(ls, file):
	output=open(file, "w")
	for element in ls:
		output.write(element)
	output.close()
	return None

###main function
input1=open(sys.argv[1], "r")
input2=open(sys.argv[2], "r")
output=open(sys.argv[3], "w")

normalized = normalize(input1)
print len(normalized)
output_ls = match_line(input2, normalized)
print len(output_ls)
write(output_ls, sys.argv[3])

input1.close()
input2.close()
output.close()




