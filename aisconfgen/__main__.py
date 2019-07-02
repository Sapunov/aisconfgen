from argparse import ArgumentParser

from .parser import Parser
from .generator import Generator


def main():

    args_parser = ArgumentParser(
        'aisconfgen', description='AIS index configuration generator')

    args_parser.add_argument(
        '-i', required=True, type=str, dest='filename',
        help='CSV file with fields')
    args_parser.add_argument(
        '-o', required=True, type=str, dest='output',
        help='File to output configuration')

    args = args_parser.parse_args()

    file_parser = Parser(args.filename)

    fields = file_parser.parse()

    config_generator = Generator(fields)

    config_generator.generate(args.output)


main()
