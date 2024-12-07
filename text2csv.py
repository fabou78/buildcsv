#! /home/fabrice/Py3venv/buildcsv/.venv/bin/python
import argparse
import csv

my_parser = argparse.ArgumentParser(
    prog='buildcsv',
    description='''Convert text from bank exported stament to CSV. The CSV
    can then later be imported into GNUcash.''',
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
my_parser.add_argument(
    '-y',
    '--year',
    help='Year to be used for the the transactions',
    type=int,
    default='2024',
    dest='year',
)

args = my_parser.parse_args()


def save_file(rows):
    with open(args.outputfile, 'w') as fileobj:
        writer = csv.writer(fileobj)
        writer.writerows(rows)
        fileobj.close()
    print(f'File {args.outputfile} has been created in the current directory')


def parse_text(file_content):
    master_list = []
    row = []
    for line in file_content:
        if 'Date' in line:
            date = line.split(':')
            if len(date) == 2:
                date = date[-1].strip()
                row.append(date)
            else:
                # If the line contain more than one ':' it will fail parsing
                print('There was an issue parsing the file')
                exit()
        if 'Description' in line:
            description = line.split(':')
            if len(description) == 2 and len(row) == 1:
                description = description[-1].strip()
                row.append(description)
            else:
                # If the line contain more than one ':' it will fail parsing
                print('There was an issue parsing the file')
                exit()
        if 'Amount' in line:
            amount = line.split(':')
            if len(amount) == 2 and len(row) == 2:
                amount = amount[-1].strip()
                row.append(amount)
                master_list.append(row)
                print(row)
                row = []
            else:
                # If the line contain more than one ':' it will fail parsing
                print('There was an issue parsing the file')
                exit()
    print(f'Found {len(master_list)} entries to import')
    save_file(master_list)


try:
    with open(args.inputfile, 'r') as fileobj:
        file_content = fileobj.readlines()
        fileobj.close()
except FileNotFoundError:
    print(f'The specified file "{args.inputfile}", does not exist')
else:
    parse_text(file_content)
