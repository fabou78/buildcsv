#! /usr/bin/python3
# This script should be installed in ~/.local/bin

import argparse
import csv

MONTH = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}


# TODO
#   get the year from the current date (using datetime.date)
#   if -y is used test that value entered is a valid 4 digit year

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


def parse_text(my_list, year):
    new_file = []
    for line in my_list:
        line = line.strip()
        items = line.split(' ')
        if len(items[0]) == 3:
            items[0] = '0' + items[0][:1]
        else:
            items[0] = items[0][:2]
        date_field = items[0] + '-' + MONTH[items[1]] + '-' + str(year)
        desc_field = ' '.join(items[2 : (len(items) - 1)])
        price_field = (items[len(items) - 1]).strip()
        price_field = price_field.replace(',', '')
        if 'CR' in desc_field:
            desc_field = desc_field.replace('CR', '').strip()
            new_line = [date_field, desc_field, price_field, None]
        else:
            new_line = [date_field, desc_field, None, price_field]
        new_file.append(new_line)
    save_file(new_file)


try:
    with open(args.inputfile, 'r') as fileobj:
        content = fileobj.readlines()
        fileobj.close()
except FileNotFoundError:
    print(f'The specified file "{args.inputfile}", does not exist')
else:
    parse_text(content, args.year)
