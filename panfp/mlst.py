"""
module: mlst
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import pandas as pd

def make_lineage_sample_table(i, o):

    """ make a lineage-sample table
        Args:
            otu-sample table
            lineage-sample table
    """

    # read an otu-sample table
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    #print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # convert an otu-sample table into a lineage-sample table
    otu_lineages = {} # the last taxon should not be undef
    for otu in otutab.index:
        lineage = otutab.loc[otu, otutab.columns[-1]]
        otu_lineages[lineage] = otu_lineages.get(lineage, 0) + 1
    print('the number of lineages = ' + str(len(otu_lineages)))

    # convert an otu-sample table into a lineage-sample table
    #lineages = sorted(otu_lineages.keys()) # should I order lineages alphabetically
    lineagesampletab = otutab.groupby(otutab.columns[-1]).sum()
    print(lineagesampletab)
    print('the number of lineage = ', str(len(lineagesampletab.index)))
    print('the number of samples = ' + str(len(lineagesampletab.columns)))

    # print a lineage-sample table
    lineagesampletab.to_csv(o, header=True, index=True, sep='\t', mode='w', float_format='%.7f')


if __name__ == "__main__":
    print(make_lineage_sample_table('test/otu_table.txt'))
