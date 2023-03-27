import random
import sys
from argparse import ArgumentParser
import argparse


class Shuf:
    # file handlers

    def __init__(self):
        self.lines = None

    def handle_restricted_repeat_file(self, file, count):
        self.read_lines_from_file(file)
        for i in range(count):
            print(random.choice(self.lines))

    def handle_restricted_shuffled_file(self, file, count):
        self.read_lines_from_file(file)
        self.shuffle_lines()
        i = count
        for line in self.lines:
            if i == 0:
                break
            i -= 1
            print(line)

    def handle_shuffled_repeat_file(self, file):
        self.read_lines_from_file(file)
        while True:
            try:
                print(random.choice(self.lines))
            except KeyboardInterrupt:
                sys.exit(0)

    def handle_shuffled_file(self, file):
        self.read_lines_from_file(file)
        self.shuffle_lines()
        self.print_lines()

    # input handlers

    def handle_shuffled_input(self):
        self.read_lines_from_input()
        self.shuffle_lines()
        self.print_lines()

    def handle_shuffled_repeat_input(self):
        # make random choices, infinitely
        self.read_lines_from_input()
        while True:
            try:
                print(random.choice(self.lines))
            except KeyboardInterrupt:
                sys.exit(0)

    def handle_restricted_repeat_input(self, count):
        # make random choices a restricted number of times
        self.read_lines_from_input()
        for i in range(count):
            print(random.choice(self.lines))

    def handle_restricted_shuffled_input(self, count):
        self.read_lines_from_input()
        self.shuffle_lines()
        i = count
        for line in self.lines:
            if i == 0:
                break
            i -= 1
            print(line)

    # echo handlers

    def handle_shuffled_echo(self, lines):
        self.lines = lines
        self.shuffle_lines()
        self.print_lines()

    def handle_shuffled_repeat_echo(self, lines):
        self.lines = lines
        while True:
            try:
                print(random.choice(self.lines))
            except KeyboardInterrupt:
                sys.exit(0)

    def handle_restricted_repeat_echo(self, lines, count):
        self.lines = lines
        for i in range(count):
            print(random.choice(self.lines))

    def handle_restricted_shuffled_echo(self, lines, count):
        self.lines = lines
        self.shuffle_lines()
        i = count
        for line in self.lines:
            if i == 0:
                break
            i -= 1
            print(line)

    # input range handlers

    def handle_shuffled_range(self, lo, hi):
        self.lines = list(range(lo, hi + 1))
        self.shuffle_lines()
        self.print_lines()

    @staticmethod
    def handle_shuffled_repeat_range(lo, hi):
        while True:
            try:
                print(random.choice(range(lo, hi + 1)))
            except KeyboardInterrupt:
                sys.exit(0)

    @staticmethod
    def handle_restricted_repeat_range(lo, hi, count):
        for i in range(count):
            print(random.choice(range(lo, hi + 1)))

    def handle_restricted_shuffled_range(self, lo, hi, count):
        self.lines = list(range(lo, hi + 1))
        self.shuffle_lines()
        i = count
        for line in self.lines:
            if i == 0:
                break
            i -= 1
            print(line)

    # specialized

    # input
    def read_lines_from_input(self):
        try:
            self.lines = sys.stdin.readlines()
        except KeyboardInterrupt:
            exit(0)
            
        self.lines = [line.replace('\n', '') for line in self.lines]

    # file
    def read_lines_from_file(self, file):
        with file as f:
            self.lines = f.readlines()
        self.lines = [line.replace('\n', '') for line in self.lines]

    # general
    def shuffle_lines(self):
        random.shuffle(self.lines)

    def print_lines(self):
        print(*self.lines, sep='\n')

    # need random lines, permuted lines, random numbers, permuted numbers


def init_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Write a random permutation of the input lines to standard output.\nWith no FILE, or when FILE "
                    "is -, read standard input.",
        epilog="Written by Arteen Abrishami"
    )

    group = parser.add_mutually_exclusive_group()

    # mutually exclusive args

    group.add_argument('-e', '--echo', action="store", metavar="args", nargs="*",
                       help="treat command-line args as input lines")
    group.add_argument('-i', '--input-range', metavar="lo-hi", action="store",
                       help="treat input as unsigned range lo-hi")
    group.add_argument('file', nargs='?', type=argparse.FileType('r'))

    # always allowed
    # parse later since of form #-# range(*rangeStr.split('-'))
    parser.add_argument('-n', '--head-count', metavar="COUNT", action="store", type=int,
                        help="output at most COUNT lines")
    parser.add_argument('-r', '--repeat', action="store_true", help="output lines can be repeated")

    # --repeat=False when not specified, all else =None

    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()
    shuf = Shuf()

    if args.head_count is not None:
        if args.head_count < 0:
            parser.error(f'invalid line count: {args.head_count}')
        elif args.head_count == 0:
            return

    # read stdin
    if not args.echo and not args.input_range and (args.file is None or args.file == sys.stdin):
        if args.head_count and args.repeat:
            shuf.handle_restricted_repeat_input(args.head_count)
        elif args.head_count:
            shuf.handle_restricted_shuffled_input(args.head_count)
        elif args.repeat:
            shuf.handle_shuffled_repeat_input()
        else:
            shuf.handle_shuffled_input()
    # read file
    elif not args.echo and not args.input_range and (args.file is not None and args.file != sys.stdin):
        if args.head_count and args.repeat:
            shuf.handle_restricted_repeat_file(args.file, args.head_count)
        elif args.head_count:
            shuf.handle_restricted_shuffled_file(args.file, args.head_count)
        elif args.repeat:
            shuf.handle_shuffled_repeat_file(args.file)
        else:
            shuf.handle_shuffled_file(args.file)
    # handle echo
    elif args.echo:
        if args.head_count and args.repeat:
            shuf.handle_restricted_repeat_echo(args.echo, args.head_count)
        elif args.head_count:
            shuf.handle_restricted_shuffled_echo(args.echo, args.head_count)
        elif args.repeat:
            shuf.handle_shuffled_repeat_echo(args.echo)
        else:
            shuf.handle_shuffled_echo(args.echo)
    # handle input range
    elif args.input_range:
        global my_range
        try:
            my_range = [int(i) for i in args.input_range.split('-')]
        except ValueError:
            parser.error("argument to input-range must be of form 'lo-hi'")

        if len(my_range) != 2:
            parser.error(f"invalid input range: {args.input_range}")

        lo, hi = my_range

        if lo > hi:
            parser.error(f"invalid input range: {args.input_range}")

        if args.head_count and args.repeat:
            shuf.handle_restricted_repeat_range(lo, hi, args.head_count)
        elif args.head_count:
            shuf.handle_restricted_shuffled_range(lo, hi, args.head_count)
        elif args.repeat:
            shuf.handle_shuffled_repeat_range(lo, hi)
        else:
            shuf.handle_shuffled_range(lo, hi)


if __name__ == "__main__":
    main()

