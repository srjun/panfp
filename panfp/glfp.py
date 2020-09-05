"""
module: glft
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import os
import re
import pandas as pd

def generate_lineage_function_profile(i, d, a, o):

    """ generate lineage functional table
    Args:
            otu-sample table
            database lineages
            annotation directory
            lineage functional profile
    """

    funcdb = a.split('/')[-1]
    if not os.path.exists(o):
        os.makedirs(o)

    # read an otu-sample table
    otutab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    #print(otutab)
    print('the number of otus = ' + str(len(otutab.index)))
    print('the number of samples = ' + str(len(otutab.columns)-1))

    otu_lineages = {} # the last taxon should not be undef
    for otu in otutab.index:
        lineage = otutab.loc[otu, otutab.columns[-1]]
        if lineage in otu_lineages:
            otu_lineages[lineage] += 1
        else:
            otu_lineages[lineage] = 1
    print('the number of lineages = ' + str(len(otu_lineages.keys())))

    # read database genomes with functional annotations
    dbs = pd.read_csv(d, sep='\t', index_col=0, header=0)

    # generate lineage functional profile by collecting organisms belonging to the lineage
    for lineage in otu_lineages.keys():
        last_taxon = lineage.split(';')[-1] # last_taxon is enough

        norgs = 0 # the number of organisms pooled for the lineage
        lineage_func = {}
        for org in dbs.index:
            db_lineage = dbs.loc[org, dbs.columns[-1]]
            if last_taxon in db_lineage:
                norgs = norgs + 1
                org_funcfile = a + '/' + org + '.' + funcdb + '.txt'
                with open (org_funcfile, 'r') as ifh:
                    for line in ifh:
                        line = line.strip()
                        # more than one functional term can be assigned
                        if len(line.split('\t')) > 1:
                            [pid, funcs] = line.split('\t')
                            for func in funcs.split(','):
                                if func in lineage_func:
                                    lineage_func[func] += 1
                                else:
                                    lineage_func[func] = 1

        if norgs > 0:
            outfile = re.sub(':', '__', lineage)
            outfile = re.sub(';', '.', outfile)
            outfile = o + '/' + outfile + '.' + funcdb + '.txt'

	    # print functional profile for lineage present in an otu-sample table
            with open (outfile, 'w') as ofh:
                ofh.write('#' + lineage + '\t' + str(norgs) +'\n')
                for func in lineage_func.keys():
                    ofh.write(func + '\t' + str(lineage_func[func]) + '\n')
        else:
            print('warning: organisms not exist for lineage, ' + lineage)


if __name__ == "__main__":
    print(generate_lineage_function_profile('test/otu_table.txt'))
