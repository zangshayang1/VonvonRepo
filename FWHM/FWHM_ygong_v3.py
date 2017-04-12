import pandas as pd
import numpy as np 
import sys 

def find_index(df, low_size, high_size):
	## find the index for the indicating range 
	size = list(df[df.columns[0]]) ## list column[0] - the list of size (bp) 
	shall_break = False
	for i in range(len(size)):  ## get the index of specified bp range 
		if shall_break is False and float(size[i]) >= float(low_size):
			low_size_index = i
			shall_break = True
		if float(size[i]) >= float(high_size):
			high_size_index = i
			break
	return low_size_index, high_size_index ## return the index of low size and high size (range)


def half_max_RFU(df, low_size_index, high_size_index):
	## create the list of min_val, which is the half_max_RFU
	min_val = []  # make empty list to store the min_val, val for half maxium 
	max_val = []  # make empty list to store the max_val, val for maxium RFU
	header = (list(df)[1:])  # list of sample names 
	for i in range(len(header)):  
		max_val.append(df[header[i]].iloc[low_size_index:high_size_index].max()) 
		max_val_array=np.array(max_val) # convert list to array 
		min_val_array=max_val_array/2 # get the half maxium RFU 
		min_val=list(min_val_array)
	return header, min_val # return sample ls_samples, ls_half_maxium_RFU


def cal_FWHM(df, header, min_val, low_size_index, high_size_index, output_name):
	## write the samples, first_position_of_half_RFU, actual_val_of_first_half_RFU,
	## second_position_of_half_RFU, acutual_val_of_second_half_RFU, FWHM
	output=open(output_name,'w') # open output file
	output.write('Sample'+'\t'+'Start_size'+'\t'+'Start_RFU'+'\t'+'End_size'+'\t'+'End_RFU'+'\t'+'FWHM'+'\n')
	size = list(df[df.columns[0]])  # make ls_bp 
	for i in range( len(header) ):
		col = df[header[i]] # make list of RFU in each sample
		col_min = min_val[i] # match the half_maxium_RFU to sample
		numbers = []
		for x in range(low_size_index, high_size_index): 
			val = col[x]
			if val > col_min: # try to find RFU that bigger than the half_maxium_RFU
				numbers.append((val, size[x])) # list [RFU_that_bigger_than_half_max, bp]
		start_val = numbers[0][0] # the first RFU that bigger than half_max
		start_idx = numbers[0][1]
		end_val = numbers[-1][0] # the last RFU that bigger than half_max
		end_idx = numbers[-1][1]
		FWHM = '{:.2f}'.format(float(end_idx)-float(start_idx)) # FWHM
		output.write(header[i]+'\t'+str(start_idx)+'\t'+str(start_val)+'\t'+str(end_idx)+'\t'+str(end_val)+'\t'+str(FWHM)+'\n')
	output.close()
	return 

###main function 
data=pd.read_csv(sys.argv[1])
low_size_index, high_size_index = find_index(data, sys.argv[3], sys.argv[4])
header, ls_half_RFU=half_max_RFU(data, low_size_index, high_size_index)
cal_FWHM(data, header, ls_half_RFU, low_size_index, high_size_index, sys.argv[2])
