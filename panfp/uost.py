"""
module: uost
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import re
import pandas as pd
from collections import OrderedDict

def update_otu_sample_table(i, d, o):
    
    """ update taxonomic information in an otu-table according to database lineages
    Args:
        otu-sample table
        database lineages
        updated otu-sample table
    """

    # attn: update undefs list whenever different undefined taxonomic annotations are found
    undefs = ['undefined', 'unclassified', 'uncultured']
    noinfo = 'undef'

    # read an otu-sample table 
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # filter otus with no taxonomic assignment
    otutab = otutab[~otutab[otutab.columns[-1]].isnull()]
    print(otutab)
    print('after removing otus with no taxonimic assignments:')
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # filter otus with zero sum
    otutab.drop(otutab.loc[otutab.iloc[:,0:len(otutab.columns)].sum(axis=1)==0].index, 
            inplace=True)
    print(otutab)
    print('after removing otus with zero sum:')
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    # read database genomes with functional annotations
    dbs = pd.read_csv(d, sep='\t', index_col=0, header=0)
    print(dbs)
    print('the number of reference genomes with taxonomy = ' + str(len(dbs.index)))

    db_lineages = {} # it should be up to species
    for lineage in dbs.loc[:, dbs.columns[-1]]:
        db_lineages[lineage] = db_lineages.get(lineage, 0) + 1
    print('the number of database lineages = ' + str(len(db_lineages.keys())))

    # modify and trim otu lineages so that the resulting lineages are compatible with
    # database lineages
    for otu in otutab.index:
        lineage = otutab.loc[otu, otutab.columns[-1]].lower()
        print('the lineage = ' + lineage)
        lineage = re.sub('\[', '', lineage) # [Clostridium]
        lineage = re.sub('\]', '', lineage) # [Clostridium]
        #delete "candidatus" because of "candidatus" deleted in database lineages
        lineage = re.sub('candidatus', '', lineage)
        print('the lineage after removing special characters = ' + lineage)

        # d,p,c,o,f,g,s for silva database
        # k,p,c,o,f,g,s for greengenes database
        # attn: we focus on only greengenes database for now
        # example taxonomic information: k__Bacteria; p__Firmicutes; c__Clostridia;
        # o__Clostridiales; f__Ruminococcaceae; g__Ruminococcus; s__bromii
        lineage2 = OrderedDict()
        lineage2 = {'k': noinfo, 'p': noinfo, 'c': noinfo, 'o': noinfo, \
                    'f': noinfo, 'g': noinfo, 's': noinfo}
        taxons = lineage.split(';')
        for taxon in taxons:
            if any(undef in taxon for undef in undefs):
                continue
            else:
                [rank, name] = taxon.split('__')
                rank = rank.strip()
                name = name.strip()
                if len(name) > 0:
                    if rank == 's':
                        lineage2[rank] = name
                    else:
                        lineage2[rank] = name.capitalize()

        # now all otus have the same length of lineage: k:xx;p:xx;c:xx;o:xx;f:xx;g:xx;s:xx
        lineage = ''
        for rank, name in lineage2.items():
            lineage = lineage + rank + ':' + name + ';'
        lineage = lineage[:-1] # remove ';'
        otutab.loc[otu, otutab.columns[-1]] = lineage
        print('the lineage after adding full ranks = ' + lineage)

        # check if lineage information exists in db lineages
        taxons_info = []
        taxons = lineage.split(';')
        for taxon in taxons:
            present = 0
            if noinfo not in taxon:
                for db_lineage in db_lineages.keys():
                    if taxon in db_lineage:
                        present = 1
                        break
            taxons_info.append(present)
        print('checking if taxonomic ranks are present in database lineages:')
        print(taxons_info)

        # keep the last level which is not 'undef'
        rank = -1
        lineage = ''
        for i in range(len(taxons_info)-1, -1, -1):
            if taxons_info[i] == 1:
                for db_lineage in db_lineages.keys():
                    if taxons[i] in db_lineage:
                        rank = i
                        idx = re.search(taxons[i], db_lineage).start()
                        lineage = db_lineage[0:idx]
                        break
                else:
                    continue
                break
        lineage = lineage + taxons[rank] # rank cannot be -1 because of k:Bacteria/k:Archaea
        print('the lineage fixing according to database lineages = ', lineage)

        # choose only otu with at least kingdom and phylum information
        if 'k:' in lineage and 'p:' in lineage:
            otutab.loc[otu, otutab.columns[-1]] = lineage
        else:
            otutab.drop([otu], inplace=True)
            print('the dropped otu = ' + otu)

    print(otutab)
    print('the number of otus after updating = ' + str(len(otutab.index)))

    # print an update otu table
    otutab.to_csv(o, header=True, index=True, sep='\t', mode='w')


if __name__ == "__main__":
    print(update_otu_sample_table('test/otu_table.txt'))
