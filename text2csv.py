#! /usr/bin/python3
# This script should be installed in ~/.local/bin

import argparse
import csv


# Defining colors for terminal
class tc:
    HEADER = '\033[95m'
    OKGRE = '\033[1;92m'
    WARN = '\033[1;93m'
    FAIL = '\033[1;91m'
    CYAN = '\033[1;36m'
    ENDC = '\033[0m'


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
    help='CSV file to write to. DEFAULT to "output.csv"',
    default='output.csv',
    dest='outputfile',
)

args = my_parser.parse_args()


def save_file(rows):
    with open(args.outputfile, 'w') as fileobj:
        writer = csv.writer(fileobj)
        writer.writerows(rows)
        fileobj.close()
    print(
        f'\nFile {tc.WARN}{args.outputfile}{tc.ENDC} has been created '
        f'in the current directory'
    )


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
                print(
                    f'\nThere was an issue parsing the date at the following line: '
                    f'{tc.FAIL}"{line.strip('\n')}"{tc.ENDC}'
                )
                exit()
        if 'Description' in line:
            description = line.split(':')
            if len(description) == 2 and len(row) == 1:
                description = (
                    description[-1].replace('&amp;', '&').replace('   ', ' ').strip()
                )
                row.append(description)
            else:
                # If the line contain more than one ':' it will fail parsing
                print(
                    f'\nThere was an issue parsing the description at the following '
                    f'line: {tc.FAIL}"{line.strip('\n')}"{tc.ENDC}'
                )
                exit()
        if 'Amount' in line:
            amount = line.split(':')
            if len(amount) == 2 and len(row) == 2:
                amount = amount[-1].replace('GBP', '').strip()
                row.append(amount)
                master_list.append(row)
                print(f'{tc.CYAN}{row}{tc.ENDC}')
                row = []
            else:
                # If the line contain more than one ':' it will fail parsing
                print(
                    f'\nThere was an issue parsing the amount at the following line: '
                    f'{tc.FAIL}"{line.strip('\n')}"{tc.ENDC}'
                )
                exit()
    print(f'\nImported {tc.OKGRE}{len(master_list)}{tc.ENDC} entries.')
    save_file(master_list)


try:
    with open(args.inputfile, 'r', encoding='iso-8859-1') as fileobj:
        file_content = fileobj.readlines()
        fileobj.close()
except FileNotFoundError:
    print(f'The specified file "{args.inputfile}", does not exist')
else:
    parse_text(file_content)
