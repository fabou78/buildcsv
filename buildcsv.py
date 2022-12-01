#! /home/fabrice/Py3venv/buildcsv/.venv/bin/python
import argparse


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


# TODO get the year from the current date (using datetime.date)

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
my_parser.add_argument(
    '-y',
    '--year',
    help='Year to be used for the the transactions',
    default='2022',
    dest='year',
)

args = my_parser.parse_args()


def parse_text(my_list, year):
    for line in my_list:
        print(line)
        # size = len(line)
        items = line.split(' ')
        if len(items[0]) == 3:
            items[0] = '0' + items[0][:1]
        else:
            items[0] = items[0][:2]

        date_field = items[0] + '-' + MONTH[items[1]] + '-' + year
        desc_field = ' '.join(items[2 : len(items) - 1])
        price_field = items[len(items) - 1]

        new_line = date_field + ',' + desc_field + ',' + price_field
        print(new_line)


try:
    with open(args.inputfile, 'r') as fileobj:
        content = fileobj.readlines()
        fileobj.close()
except FileNotFoundError:
    print(f'The specified file "{args.inputfile}", does not exist')
else:
    parse_text(content, args.year)
