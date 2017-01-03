#bin/bash/python
import sys
import numpy as np

class OverlapLine(object):
	def __init__(self, line, separator = '\t'):
		splitted_line = line.rstrip().split(separator)
		self.chrom_name = splitted_line[0]
		self.start1 = int(splitted_line[1])
		self.end1 = int(splitted_line[2])
		self.start2 = int(splitted_line[13])
		self.end2 = int(splitted_line[14])

# to accelerate writing out ...
class myStringBuilder(object):
	def __init__(self):
		self.content = []
	def append(self, newline):
		self.content.append(newline)
		return ;


def read_chromosome_size(path, separator = '\t'):
	# input: uscs hg38.chrom.sizes file containing two column separated by '\t'
	# 		 column1: chromosome name
	# 		 column2: chromosome size
	# output: a dict holding each chromosome name as a key followed by an np.array of the same size as the chromosome
	
	f = open(path, 'r')
	coverage = {}
	for line in f:
		chrom_name = line.rstrip().split(separator)[0]
		length = int(line.rstrip().split(separator)[1])
		coverage[chrom_name] = np.zeros(length)
	return coverage

def read_overlap_input(path):
	# input: overlap input file
	# output: a list of OverlapLine() objects
	f = open(path, 'r')
	content =  f.readlines()
	assert len(content) > 1, "ERROR: overlap file"
	alist = [None for _ in range(len(content))]
	for i, line in enumerate(content):
		alist[i] = OverlapLine(line)
	return alist

def calc_overlap(o):
	# input: OverlapLine() object
	# output: overlapped start and end positions in tuple
	start = max(o.start1, o.start2)
	end = min(o.end1, o.end2)
	return (start, end)

def calc_coverage(coverage, olist):
	# input: empty dict - coverage
	# 		 OverlapLine object list - olist
	# output: dict with right coverage at the right position
	for o in olist:
		s, e = calc_overlap(o)
		while s <= e:
			cur_chrom = coverage[o.chrom_name]
			cur_chrom[s] += 1
			s += 1
	return coverage




def output_coverage_wrapper(cover_dict, olist, output_filepath, separator = '\t'):
	# input: overlap input list
	# 		 calculated coverage dict
	# output: outputfile with coverage in the following format:
	# 		  column1: chrom_name
	# 		  column2: covered position
	# 		  column3: normalized position
	# 		  column4: coverage
	# 		  column5: target label

	sb = myStringBuilder()

	for i in range(len(olist)):
		
		o = olist[i]
		start, end = calc_overlap(o)
		overlap_length = end - start + 1
		assert overlap_length > 0, "ERROR: non-overlap detected."

		pos_incrementer = 1.0
		while start <= end:
			chrom_name = o.chrom_name
			pos_normalized = pos_incrementer / overlap_length
			pos = start
			coverage = cover_dict[chrom_name][start]
			target_idc = i + 1
			newline = (str(chrom_name) + separator 
						+ str(pos) + separator 
						+ str(pos_normalized) + separator 
						+ str(coverage) + separator
						+ str(target_idc)
						)
			sb.append(newline)
			start += 1
			pos_incrementer += 1
	
	print "creating output ..."

	outputfile = open(output_filepath, 'w')
	header = "Chrom" + separator + "Pos" + separator + "Pos_normalized" + separator + "Coverage" + separator + "Target"
	outputfile.write(header + '\n')
	outputfile.write('\n'.join(sb.content))
	outputfile.close()
	return ;

def main():
	# sys.argv[1] - hg38.chrom.sizes downloaded from UCSB server
	# sys.argv[2] - overlap input file
	# sys.argv[3] - output path + name
	print "start ..."
	print "running ..."
	coverage_dict = read_chromosome_size(sys.argv[1])
	print "chromosome size cached."
	print "running ..."
	olist = read_overlap_input(sys.argv[2])
	print "overlapped reads cached."
	print "running ..."
	coverage_dict = calc_coverage(coverage_dict, olist)
	print "coverage cached."
	print "running ..."
	output_coverage_wrapper(coverage_dict, olist, sys.argv[3])
	print "output done!"
	return ;


if __name__ == '__main__':
	main()
















