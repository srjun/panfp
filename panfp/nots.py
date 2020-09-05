"""
module: nots
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import pandas as pd

def normalize_otu_sample_table_by_sequencing_depth(i, o):

    """ normalize an otu-sample table by sequencing depth
        Args:
            otu-sample table
            normalized otu-sample table
    """

    # read an otu-sample table
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    #print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # calculate sequencing depth
    sample_depth = {}
    print('sample\tsequencing depth')
    for sample in otutab.columns[0:-1]:
        depth = otutab[sample].sum()
        sample_depth[sample] = depth
        print(sample + '\t' + str(depth))

    # normalize an otu-sample table by sequencing depth
    for sample in otutab.columns[0:-1]:
        depth = sample_depth[sample]
        for otu in otutab.index:
            # in percentage
            otutab.loc[otu, sample] = (otutab.loc[otu, sample]/depth)*100

    # print an otu-table normalized by sequencing depth
    #pd.options.display.float_format = "{:,.7f}".format
    # it seems that the last column (strings) doesn't raise error by float_format
    otutab.to_csv(o, header=True, index=True, sep='\t', mode='w', float_format='%.7f')


if __name__ == "__main__":
    print(normalize_otu_sample_table_by_sequencing_depth('test/otu_table.txt'))

