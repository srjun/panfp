#!/usr/bin/env python3

"""
module: panfp
module author: Se-Ran Jun - All Rights Reserved
last updated: 09/01/2020
"""

import os
import sys
import argparse


def run_panfp():
    commands = {'uost': update_otu_sample_table,
                'clct': calculate_lineage_copynum_table,
                'glfp': generate_lineage_function_profile,
                'notc': normalize_otu_sample_table_by_copynum,
                'nots': normalize_otu_sample_table_by_sequencing_depth,
                'mlst': make_lineage_sample_table,
                'mfst': make_function_sample_table
               }

    # argument parser
    parser = argparse.ArgumentParser(
        description='Pangenome-based metagenome prediction',
        usage="""panfp <command> [<args>]

Commands can be:
uost <filenames>      Update an otu-sample table
clct <filenames>      Calculate lineage copy number table
glfp <filenames>      Generate functional profiles for lineages from an otu-sample table
notc <filenames>      Normalize an otu-sample table by copy number
nots <filenames>      Normalize an otu-sample table by sequencing depth
mlst <filenames>      Make a lineage-sample table
mfst <filenames>      Make a function-sample table
""")

    parser.add_argument('command')
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in commands:
        parser.print_help()
        sys.exit(1)

    cmd = commands.get(args.command)
    cmd(sys.argv[2:])


def update_otu_sample_table(args):

    from panfp.uost import update_otu_sample_table

    """ update taxonomic information in an otu-table according to database lineages
    Args:
        otu-sample table
        database lineages
        updated otu-sample table
    """

    #print(args)

    parser = argparse.ArgumentParser(description='update an otu-sample table')
    parser.add_argument('-i', '--input', 
                        required=True,
                        type=str, 
                        help='otu-sample table')
    parser.add_argument('-d', '--database', 
                        required=True,
                        type=str, 
                        help='database lineages')
    parser.add_argument('-o', '--output', 
                        required=True,
                        type=str,
                        help='updated otu-sample table')
    args = parser.parse_args(args)

    #print(args)
    update_otu_sample_table(args.input, args.database, args.output)


def calculate_lineage_copynum_table(args):

    from panfp.clct import calculate_lineage_copynum_table

    """ calculate copy number for each lineage in an otu-sample table
    Args:
        otu-sample table
        database lineages
        lineage copynumber table
    """

    parser = argparse.ArgumentParser(description='calculate lineage copy number')
    parser.add_argument('-i', '--input', 
                        required=True,
                        type=str, 
                        help='otu-sample table')
    parser.add_argument('-d', '--database', 
                        required=True,
                        type=str, 
                        help='database lineages')
    parser.add_argument('-o', '--output', 
                        required=True,
                        type=str, 
                        help='lineage copynumber table')
    args = parser.parse_args(args)

    #print(args)
    calculate_lineage_copynum_table(args.input, args.database, args.output)


def generate_lineage_function_profile(args):

    from panfp.glfp import generate_lineage_function_profile

    """ generate lineage functional profile
    Args:
        otu-sample table
        database lineages
        annotation directory
        lineage functional profile
    """

    parser = argparse.ArgumentParser(description='generate lineage functional profile')
    parser.add_argument('-i', '--input', 
                        required=True,
                        type=str, 
                        help='otu-sample table')
    parser.add_argument('-d', '--database', 
                        required=True,
                        type=str, 
                        help='database lineages')
    parser.add_argument('-a', '--annotdir', 
                        required=True,
                        type=str, 
                        help='annotation directory')
    parser.add_argument('-o', '--output',
                        required=True,
                        type=str, 
                        help='lineage functional profile')
    args = parser.parse_args(args)

    #print(args)
    generate_lineage_function_profile(args.input, args.database, args.annotdir, args.output)


def normalize_otu_sample_table_by_copynum(args):

    from panfp.notc import normalize_otu_sample_table_by_copynum

    """ normalize an otu-sample table by copy number
    Args:
        otu-sample table
        lineage copy number table
        normalized otu-sample table
    """

    parser = argparse.ArgumentParser(description='normalize an otu-sample table by copy number')
    parser.add_argument('-i', '--input', 
                        required=True,
                        type=str, 
                        help='otu-sample table')
    parser.add_argument('-c', '--lineagecopynum', 
                        required=True,
                        type=str, 
                        help='lineage copy number table')
    parser.add_argument('-o', '--output', 
                        required=True,
                        type=str, 
                        help='normalized otu-sample table')
    args = parser.parse_args(args)

    #print(args)
    normalize_otu_sample_table_by_copynum(args.input, args.lineagecopynum, args.output)


def normalize_otu_sample_table_by_sequencing_depth(args):

    from panfp.nots import normalize_otu_sample_table_by_sequencing_depth

    """ normalize an otu-sample table by sequencing depth
    Args:
        otu-sample table
        normalized otu-sample table
    """

    parser = argparse.ArgumentParser(description='normalize an otu-sample table by sequencing depth')
    parser.add_argument('-i', '--input', type=str, help='otu-sample table')
    parser.add_argument('-o', '--output', type=str, help='normalized otu-sample table')
    args = parser.parse_args(args)

    #print(args)
    normalize_otu_sample_table_by_sequencing_depth(args.input, args.output)


def make_lineage_sample_table(args):

    from panfp.mlst import make_lineage_sample_table

    """ make a lineage sample table
    Args:
        otu-sample table
        lineage-sample table
    """

    parser = argparse.ArgumentParser(description='make a lineage-sample table')
    parser.add_argument('-i', '--input', 
                        required=True,
                        type=str, 
                        help='otu-sample table')
    parser.add_argument('-o', '--output', 
                        required=True,
                        type=str, 
                        help='lineage-sample table')
    args = parser.parse_args(args)

    #print(args)
    make_lineage_sample_table(args.input, args.output)


def make_function_sample_table(args):

    from panfp.mfst import make_function_sample_table

    """ make a function sample table
    Args:
        lineage-sample table
        lineage functional profiles
        function-sample table
    """

    parser = argparse.ArgumentParser(description='make a function-sample table')
    parser.add_argument('-i', '--input', type=str, help='lineage-sample table')
    parser.add_argument('-f', '--funcdir', type=str, help='lineage functional profiles')
    parser.add_argument('-o', '--output', type=str, help='function-sample table')
    args = parser.parse_args(args)

    #print(args)
    make_function_sample_table(args.input, args.funcdir, args.output)


if __name__ == "__main__":
    run_panfp()
