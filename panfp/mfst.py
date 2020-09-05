"""
module: mfst
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import re
import datetime
import numpy as np
import pandas as pd


def make_function_sample_table(i, f, o):

    """ make a function-sample table
        Args:
            lineage-sample table
            lineage functional profiles
            function-sample table
    """

    time_start = datetime.datetime.now()
    print(time_start)

    funcdb = f.split('/')[-1]
    #print(funcdb)

    # read a lineage-sample table
    lineagesampletab = pd.read_csv(i, sep='\t', index_col=0, header=0)
    #print(lineagesampletab)
    samples = lineagesampletab.columns
    lineages = lineagesampletab.index
    print('the number of lineages = ' + str(len(lineages)))
    print('the number of samples = ' + str(len(samples)))

    # read functional profiles for lineages
    all_funcs = {}
    lineage_func = {}
    # lineage_func should have the same order of lineages as in lineage-sample table
    # for matrix multiplication
    for lineage in lineages:
        lineage_func[lineage] = {}
        #print(lineage)

        infile = re.sub(':', '__', lineage)
        infile = re.sub(';', '.', infile)
        infile = f + '/' + infile + '.' + funcdb + '.txt'
        with open (infile, 'r') as ifh:
            for line in ifh:
                line = line.strip()
                if line.startswith('#'):
                    [taxon, norgs] = line.split('\t')
                    taxon = taxon[1:]
                else:
                    [func, freq] = line.split('\t')
                    lineage_func[lineage][func] = float(freq)/float(norgs)
                    #print(func + '\t' + str(norgs) + '\t' + str(freq) + '\t' + str(lineage_func[lineage][func]))

                    if func not in all_funcs:
                        all_funcs[func] = 1
    sorted_all_funcs = sorted(all_funcs.keys())
    print('the number of functions = ' + str(len(sorted_all_funcs)))

    lineage_func_df = pd.DataFrame.from_dict(lineage_func, orient='index').replace(np.nan, 0)
    lineage_func_df = lineage_func_df.reindex(index=lineages)
    lineage_func_df = lineage_func_df.reindex(columns=sorted_all_funcs)
    print(lineage_func_df)

    # make a function sample table by plug-in lineages' functional profiles after normalizing
    # the occurrence of functional terms by the number of organisms belonging to lineages

    #funcsampletab = pd.DataFrame(index=sorted_all_funcs, columns=samples, dtype='float64')
    #funcsampletab.index.name = 'function'
    #for func in sorted_all_funcs:
    #    for sample in samples:
    #
    #        funcsampletab.loc[func, sample] = 0.0
    #        for lineage in lineagesampletab.index:
    #            if func in lineage_func[lineage]:
    #                val = lineagesampletab.loc[lineage, sample] * lineage_func[lineage][func]
    #                funcsampletab.loc[func, sample] += val

    lineage_func_m = lineage_func_df.to_numpy()
    func_lineage_m = lineage_func_m.transpose()
    lineage_sample_m = lineagesampletab.to_numpy()
    #print(lineage_func_m.shape)
    #print(func_lineage_m.shape)
    #print(lineage_sample_m.shape)
    funcsampletab_m = np.matmul(func_lineage_m, lineage_sample_m)
    funcsampletab_df = pd.DataFrame(data=funcsampletab_m.astype(float))
    funcsampletab_df.index = sorted_all_funcs
    funcsampletab_df.index.name = 'function'
    funcsampletab_df.columns = samples

    # print a function-sample table
    funcsampletab_df.to_csv(o, header=True, index=True, sep='\t', mode='w', float_format='%.7f')

    time_end = datetime.datetime.now()
    print(time_end)
    time_elapsed = time_end - time_start
    print(time_elapsed)


if __name__ == '__main__':
    print(make_function_sample_table('test/otu_table.txt'))
