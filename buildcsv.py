#! /home/fabrice/Py3venv/buildcsv/.venv/bin/python
import argparse


my_parser = argparse.ArgumentParser(
    prog='buildcsv',
    description='Convert text from bank export to csv',
    allow_abbrev=False,
)
my_parser.add_argument(
    '-i', '--input', help='Text file to import', required=True, dest='inputfile'
)
my_parser.add_argument(
    '-o',
    '--output',
    help='csv file to write to',
    default='output.csv',
    dest='outputfile',
)

args = my_parser.parse_args()

print(vars(args))
