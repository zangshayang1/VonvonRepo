
for ID in SR_120_1 SR_120_2 SR_120M_1 SR_120M_2
do
	echo $ID
	python /grail/scratch/excalibur/rocket/user/ygong/IDT/coverage_of_probe_by_base/011717_SR_120v80_cfDNA/probe_and_coverage_each_base.py /grail/scratch/excalibur/rocket/techdev_analysis/170110_E00498_0035_AH7N2TALXX/KS_Pecan/cfDNA_80v120_4Msub/results/$ID/variantcalling/pileup/${ID}.collapsed.tsv 120mer_coverage_pos.txt ${ID}_pos_coverage.txt
done
