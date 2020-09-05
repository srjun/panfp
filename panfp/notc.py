"""
module: notc
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import pandas as pd

def normalize_otu_sample_table_by_copynum(i, c, o):

    """ normalize an otu-sample table by copy number
        Args:
            otu-sample table
            lineage copy number table
            normalized otu-sample table
    """

    # read an otu-sample table
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    #print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # read copy numbers for lineages present in the otu-table
    # will take median of copy numbers for each lineage
    lineage_copynum = pd.read_csv(c, sep='\t', index_col=0, header=0)
    print(lineage_copynum.columns)
    print('the number of lineages = ' + str(len(lineage_copynum.index)))

    # normalize the otu-sample table by median copy number
    for otu in otutab.index:
        # it should be full lineage (not just last taxon)
        otu_lineage = otutab.loc[otu, otutab.columns[-1]]
        print(otu_lineage)
        chk = 0
        for lineage in lineage_copynum.index:
            if otu_lineage == lineage: # it should be exact match
                chk = 1
                copynum = lineage_copynum.loc[lineage, 'median'] # median
                print(lineage + '\t' + str(copynum))
                for sample in otutab.columns[0:-1]:
                    #print(otu + '\t' + sample)
                    otutab.loc[otu, sample] = otutab.loc[otu, sample]/copynum
                break
        # this step might not be necessary since the otu-sample table was updated 
        if chk == 0:
            print('warning: the otu which will be removed = ' + otu)
            otutab.drop(otu, axis=0, inplace=True)

    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # print an otu-table normalized by lineage copy number
    otutab[otutab.columns[0:-1]] = otutab[otutab.columns[0:-1]].astype(int)
    otutab.to_csv(o, header=True, index=True, sep='\t', mode='w') 
    

if __name__ == "__main__":
    print(normalize_otu_sample_table_by_copynum('test/otu_table.txt'))
