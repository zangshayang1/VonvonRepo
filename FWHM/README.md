This script is to evaluate the tightness of FA trace by comparing Full Width at Half Maximum (FWHM.) 

Sample command to run the script is "python FWHM_ygong_v*.py Sample_input.csv Sample_output.txt low_range high_range"

About V6:
One column called “Peak” is added into the output file, which is the peak location(bp) of the sample
Use interpolation package to transfer the float bp to integer bp, and predict the y - RFU
Besides the final output, the intermediate output with integer bp is generated
example: python FWHM_ygong_v6.py input.csv int_output.csv final_output.csv low_size high_size" 
