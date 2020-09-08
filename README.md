---

<p align="center">
  <img src=".logo/pangenome.png"/>
</p>

PanFP is a Python pipeline to predict pangenome-based functional profiles for microbial communities.

## Requirements
Specific libraries are required by PanFP. We provide a [requirements](./requirements.txt) file to install everything at once. To do so, you will need first to have [pip](https://pip.pypa.io/en/stable/installing/) installed and then run:

```bash
pip3 --version                      # Check if installed
sudo apt-get install python3-pip    # if you need to install pip, you can check installation with the previous command
pip3 install -r requirements.txt

```

## Installation & Help

Download this repository and run:

```bash
python3 setup.py install
```

You may require to call it using sudo. Once installed, panfp`should be available anywhere in your terminal.

In the case you need to install the package in a specific directory of your system, you can call the argument *--install-lib* followed by a directory path:

```bash
python3 setup.py install --install-lib /custom/path/
```
## Example

Requirements to run an experiment are: 

-d [database of reference genomes with functional annotation] \[[here](./dbs/refseq.complete.KO.TH30.txt)\] <br />
-a [directory which contains functional profiles of genomes in database] \[[here](./annot/KO)\] <br />
-i [otu-sample table] <br /> 

To see additional arguments:
```bash
bin/panfp --help
```

As example, we included an example script \[[here](./run_panfp.sh)\] with a full workflow of how panfp works and an example otu-sample table \[[here](./test/otu_table.txt)\].

Note that an input, otu-sample table should be in a tab delimited format as follows:

|\#OTU ID|S1   |S2   |...  |S10  |Lineage |
|:-------|:----|:----|:----|:----|:-------|
|OTU_1   |0.0  |10.0 |...  |2.0  |k__Bacteria; p__Proteobacteria; c__Betaproteobacteria; o__MND1; f__|
|OTU_2   |4.0  |430.0|...  |24.0 |k__Bacteria; p__Proteobacteria; c__Betaproteobacteria; o__; f__; g__; s__|
|...     |...  |...  |...  |...  |k__Bacteria;p__Cyanobacteria;c__Oxyphotobacteria|
|OTU_99  |1.0  |5.0  |...  |0.0  |k__Bacteria;p__Chloroflexi;c__|
|OTU_100 |0.0  |35.0 |...  |2.0  |k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Enterobacteriales; f__Enterobacteriaceae; g__Gluconacetobacter; s__liquefaciens|

where the first column represents OTU ids, numbers represent raw frequency of 16S rRNA, and the last column represents lineage of OTUs.

As example, we included an example script \[[here](./run_panfp.sh)\] with a full workflow of how panfp works and an example otu-sample table \[[here](./test/otu_table.txt)\].

##  Output Information:

The following files are generated in the following order:

- updated_otu_table.txt - otu-sample table with updated taxonomic information according to database lineages \[[example](./test/results/updated_otu_table.txt)\]
- lineage_copynum.txt - copy numbers for lineages in an updated otu-sample table \[[example](./test/results/lineage_copynum.txt)\]
- for example, k__Bacteria.p__Ignavibacteriae.c__Ignavibacteria.KO.txt - functional profiles for lineages \[[example](./test/results/lineage_func/KO/k__Bacteria.p__Ignavibacteriae.c__Ignavibacteria.KO.txt)\]
- updated_otu_table_norm_by_copynum.txt - otu-sample table normalized by median copy numbers of lineages \[[example](./test/results/updated_otu_table_norm_by_copynum.txt)\]
- updated_otu_table_norm_by_copynum_depth.txt - otu-sample table normalized by sequencing depth \[[example](./test/results/updated_otu_table_norm_by_copynum_depth.txt)\]
- lineage_sample_table.txt - lineage-sample table derived from otu-sample table grouping by lineages \[[example](./test/results/lineage_sample_table.txt)\]
- function_sample_table.txt - funciton-sample table by multiplying lineage-sample table and lineage-function table \[[example](./test/results/function_sample_table.txt)\]

## Contact

This project has been fully developed at the group of [Translational Bioinformatics - Jun Lab](http://abc.srjun.tbi.org).

If you experience any problem at any step involving the program, you can use the 'Issues' page of this repository or contact: [Se-Ran Jun](mailto:seran.jun@gmail.com)


## License

PanFP is under a common GNU GENERAL PUBLIC LICENSE. Plese, check [LICENSE](./LICENSE) for further information.

###### [2020] - Se-Ran Jun - All Rights Reserved*
