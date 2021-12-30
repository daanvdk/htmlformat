from argparse import ArgumentParser, FileType
from .parser import parse
from .renderer import render


parser = ArgumentParser(description='format html')
parser.add_argument('input', type=FileType('r'), nargs='?', default='-')
parser.add_argument('-o', '--output', type=FileType('w'), default='-')


def main():
    args = parser.parse_args()
    content = args.input.read()
    content = render(parse(content))
    args.output.write(content)


if __name__ == '__main__':
    main()
