#!/bin/bash

#step1:
bin/panfp uost -i test/otu_table.txt -d dbs/refseq.complete.KO.TH30.txt -o test/results/updated_otu_table.txt

#step2:
bin/panfp clct -i test/results/updated_otu_table.txt -d dbs/refseq.complete.KO.TH30.txt -o test/results/lineage_copynum.txt

#step3:
bin/panfp glfp -i test/results/updated_otu_table.txt -d dbs/refseq.complete.KO.TH30.txt -a annot/KO -o test/results/lineage_func/KO

#step4:
bin/panfp notc -i test/results/updated_otu_table.txt -c test/results/lineage_copynum.txt -o test/results/updated_otu_table_norm_by_copynum.txt

#step5:
bin/panfp nots -i test/results/updated_otu_table_norm_by_copynum.txt -o test/results/updated_otu_table_norm_by_copynum_depth.txt

#step6:
bin/panfp mlst -i test/results/updated_otu_table_norm_by_copynum_depth.txt -o test/results/lineage_sample_table.txt

#step7:
bin/panfp mfst -i test/results/lineage_sample_table.txt -f test/results/lineage_func/KO -o test/results/function_sample_table.txt
