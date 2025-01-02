import argparse
import sys


class Config:
    def __init__(self):
        self.paginate: bool = False
        self.lines_per_page: int = None

        self.argv: int = None

    def parse(self):
        parser = argparse.ArgumentParser(
            prog='popa', description='Exhentai CLI client'
        )

        parser.add_argument(
            '-p',
            '--paginate',
            help='Enable pagination with lines for each page (default: 40)',
        )

        args = parser.parse_args()

        if args.paginate is None:
            self.lines_per_page = 40
        else:
            self.paginate = True
            self.lines_per_page = int(args.paginate)

        self.argv = len(sys.argv)

CONF = Config()
