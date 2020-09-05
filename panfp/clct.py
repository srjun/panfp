"""
module: ccnl
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import pandas as pd
import numpy as np

def calculate_lineage_copynum_table(i, d, o):

    """ calculate copy number for each lineage in an otu-sample table
    Args:
        otu-sample table
        database lineages
        lineage copynumber table
    """

    # read an otu-sample table
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # read database genomes with functional annotations
    dbs = pd.read_csv(d, sep='\t', index_col=0, header=0)
    print(dbs)
    print('the number of reference genomes with taxonomy = ' + str(len(dbs.index)))

    otu_lineages = {} # the last taxon should not be undef
    for otu in otutab.index:
        lineage = otutab.loc[otu, otutab.columns[-1]]
        if lineage in otu_lineages:
            otu_lineages[lineage] += 1
        else:
            otu_lineages[lineage] = 1

    # make copy number distribution for each lineage
    ridx = 0
    lineage_copynum = pd.DataFrame(columns=['lineage','mean','median','copynum'])
    for lineage in otu_lineages:
        # last taxon must be present in database lineages
        last_taxon = lineage.split(';')[-1] # it should not be undef

        copynums = []
        for organism in dbs.index:
            # -1 is the column index for taxonomy
            db_lineage = dbs.loc[organism, dbs.columns[-1]]
            if last_taxon in db_lineage:
                # 1 is the column index for copy number
                copynum = dbs.loc[organism, dbs.columns[1]]
                copynums.append(copynum)

        # is it possible to have empty copy numbers?
        if len(copynums) > 0:
            val1 = '{:.1f}'.format(np.mean(copynums))
            val2 = np.median(copynums)
            dcopynums =','.join(map(str, copynums))
            lineage_copynum.loc[ridx] = [lineage, val1, val2, dcopynums]
            ridx = ridx + 1
        else:
            print('warning: no organism in db which belongs to the taxon' + lineage)

    # print copy number distributions for lineages in an otu-sample table
    lineage_copynum.to_csv(o, header=True, index=False, sep='\t', mode='w')


if __name__ == "__main__":
    print(calculate_lineage_copynum_table('test/otu_table.txt'))
