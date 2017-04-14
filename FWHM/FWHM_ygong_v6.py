import pandas as pd
import numpy as np 
import sys 
import time 
from scipy import interpolate
import functools

def int_extrapolation(df, low_size, high_size, int_output_name):

	dt = pd.read_csv(sys.argv[1])#read data table

	header = list(dt.ix[0:1])[1:]#put the sample names into list, [0:1] is the first row, [1:]means start from the second
	lst = [] #make empty list 
	lst1 = []
	for item in header:
		frame = pd.DataFrame({'bp': dt['Size (bp)'],item : dt[item]})
		data = pd.DataFrame({'bp':frame['bp'],item : frame[item]}) #above two lines are the same function
		x = data['bp']
		y = data[item]
		tck = interpolate.splrep(x,y,s = 0) #interpolate 
		xnew = np.arange(int(low_size), int(high_size)+1) #set x range
		ynew = interpolate.splev(xnew,tck,der = 0) #return the predicted y, derivative is 0 
		zynew = [0 if y < 0 else y for y in ynew] #make the negative RFU as 0 
		new = pd.DataFrame({'bp':xnew,item:[0 if y < 0 else y for y in ynew]}, columns = ['bp', item]) #acutally, to me this lane can use zynew directly
		normalized_rfu = [x1/float(np.sum(zynew)) for x1 in zynew]
		b = pd.DataFrame({'bp': xnew, item : normalized_rfu} , columns  = ['bp' , item])
		lst.append(new) 
		lst1.append(b)
		df_final = functools.reduce(lambda left,right: pd.merge(left,right,on=['bp']), lst) #combine the data of RFU at integer bp
		df = functools.reduce(lambda left,right: pd.merge(left,right,on=['bp']), lst1) #combine the data of normalized RFU (actual/total)
	int_output = df_final.to_csv(int_output_name, index=False)
	return int_output, df_final


def find_index_binary(df, low_size, high_size):
	## find the index for the indicating range 
	size = list(df[df.columns[0]])
	# use binary theory to find the first index that is bigger than low_size or high_size
	start_low = 0
	end_low = len(size) - 1
	while start_low < end_low:
		mid = (start_low + end_low)//2
		if float(size[mid]) < float(low_size):
			start_low = mid+1
		else: 
			end_low = mid

	start_high = 0
	end_high = len(size) - 1
	while start_high < end_high:
		mid = (start_high + end_high)//2
		if float(size[mid]) < float(high_size):
			start_high = mid + 1
		else:
			end_high = mid

	return end_low, end_high
	

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
	return header, min_val, max_val # return sample ls_samples, ls_half_maxium_RFU, ls_maxium_RFU


def cal_FWHM(df, header, min_val, max_val, low_size_index, high_size_index, output_name):
	## write the samples, first_position_of_half_RFU, actual_val_of_first_half_RFU,
	## second_position_of_half_RFU, acutual_val_of_second_half_RFU, FWHM
	output=open(output_name,'w') # open output file
	output.write('Sample'+'\t'+'Start_size'+'\t'+'Start_RFU'+'\t'+'End_size'+'\t'+'End_RFU'+'\t'+'FWHM'+'\t'+ 'Peak' + '\n')
	size = list(df[df.columns[0]])  # make ls_bp 
	for i in range( len(header) ):
		col = df[header[i]] # make list of RFU in each sample
		col_min = min_val[i] # match the half_maxium_RFU to sample
		col_max = max_val[i]
		numbers = []
		numbers_max=[]
		for x in range (low_size_index, high_size_index): #this is to find the bp of the peak (max_RFU)
			val = col[x]
			if float(val) == float(col_max):
				numbers_max.append(size[x])
		for x in range(low_size_index, high_size_index): 
			val = col[x]
			if val > col_min: # try to find RFU that bigger than the half_maxium_RFU
				numbers.append((val, size[x])) # list [RFU_that_bigger_than_half_max, bp]
		start_val = numbers[0][0] # the first RFU that bigger than half_max
		start_idx = numbers[0][1]
		end_val = numbers[-1][0] # the last RFU that bigger than half_max
		end_idx = numbers[-1][1]
		max_bp = numbers_max[0]
		FWHM = '{:.2f}'.format(float(end_idx)-float(start_idx)) # FWHM
		output.write(header[i]+'\t'+str(start_idx)+'\t'+str(start_val)+'\t'+str(end_idx)+'\t'+str(end_val)+'\t'+str(FWHM)+'\t'+str(max_bp)+'\n')
	output.close()
	return 

###main function 
data=pd.read_csv(sys.argv[1])
#a_1 = time.time()
#print (a_1-a_0)## this is to find out the time used for each function 
int_out_csv, data_int = int_extrapolation(data, sys.argv[4], sys.argv[5], sys.argv[2])

low_size_index, high_size_index= find_index_binary(data_int, sys.argv[4], sys.argv[5])
#a_2 = time.time()
#print (a_2-a_1)
header, ls_half_RFU, ls_max_RFU=half_max_RFU(data_int, low_size_index, high_size_index)
#a_3 = time.time()
#print (a_3 - a_2)
cal_FWHM(data_int, header, ls_half_RFU, ls_max_RFU, low_size_index, high_size_index, sys.argv[3])
#a_4 = time.time()
#print (a_4 - a_3)
