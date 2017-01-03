#!/bin/bash/python

import sys
import os

COL_SAMPLE_ID = "sample_id"
COL_FASTQ1 = "fastq_1"
COL_FASTQ2 = "fastq_2"
COL_MANIFEST = "manifest"
COL_NRUMI = "nrumi"
COL_SUBSAMPLE_FRACTION = "subsample_fraction"

CHECK_1 = "R1"
CHECK_2 = "R2"



class VonTableGenerator(object):
	def __init__(self, path, unique_identifier, manifest, nrumi, outfile_name):
		self.path = path
		self.uid = unique_identifier
		self.manifest = manifest
		self.nrumi = nrumi
		self.outfile_name = outfile_name
		self.subsample_fraction = []
		self.fastq_pool = []

	def pool_fastq_on_unique_identifier(self):
		for fastqfile_name in os.listdir(self.path):
			if not self.uid in fastqfile_name:
				continue
			self.fastq_pool.append(fastqfile_name)

		self.fastq_pool = sorted(self.fastq_pool)
		return;

	def generate_id_labels(self):
		if len(self.fastq_pool) == 0 or len(self.fastq_pool) % 2 == 1:
			raise Exception("Error occurred in pooling fastq step.")

		for i in xrange(0, len(self.fastq_pool), 2):
			self.fastq_pool[i]
		# --------------------------------------------------------------------------------------------------

	def create_output(self):		
		if len(self.fastq_list) != 2 * len(self.ids):
			raise Exception("ERROR: numbers of existing samples doesn't pair up with given sample IDs.")

		outfile = open(self.outfile_name, 'w')
		# create header according to config
		outfile.write(COL_SAMPLE_ID + '\t' 
					+ COL_FASTQ1 + '\t' 
					+ COL_FASTQ2 + '\t' 
					+ COL_MANIFEST + '\t' 
					+ COL_NRUMI + '\t' 
					+ COL_SUBSAMPLE_FRACTION + '\n')
		
		for i in xrange(len(self.ids)):
			
			outfile.write(self.ids[i].rstrip() + '\t')

			if not CHECK_1 in self.fastq_list[2 * i]:
				raise Exception("ERROR: sample name failed R1 CHECK.")
			else:
				outfile.write(self.fastq_list[2 * i].rstrip() + '\t')
			
			if not CHECK_2 in self.fastq_list[2 * i + 1]:
				raise Exception("ERROR: sample name failed R2 CHECK.")
			else:
				outfile.write(self.fastq_list[2 * i + 1].rstrip() + '\t')

			if len(self.subsample_fraction) == 0:
				outfile.write(self.manifest + '\t' + self.nrumi + '\t' + '0' + '\n')
			else:
				raise Exception("Under dev...")
		outfile.close()
		return;


def main():
	path = sys.argv[1]
	manifest = sys.argv[2]
	nrumi = sys.argv[3]
	outfile_name = sys.argv[4]
	with open(sys.argv[5], 'r') as ids_file:
		ids = ids_file.readlines()
	subsample_fraction = []
	
	vonTableGenerator = VonTableGenerator(path, manifest, nrumi, outfile_name, ids, subsample_fraction)
	vonTableGenerator.collect_fastq()
	vonTableGenerator.create_output()

	return;

main()
