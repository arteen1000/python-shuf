# python-shuf
Based on GNU shuf, but Python implementation. Find implementation in `shuf.py`. 

Here is the help message:

```
$ python3 shuf.py --help
usage: shuf.py [-h] [-e [args ...]] [-i lo-hi] [-n COUNT] [-r] [file]

Write a random permutation of the input lines to standard output. With no FILE, or when FILE is -, read standard input.

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  -e [args ...], --echo [args ...]
                        treat command-line args as input lines
  -i lo-hi, --input-range lo-hi
                        treat input as unsigned range lo-hi
  -n COUNT, --head-count COUNT
                        output at most COUNT lines
  -r, --repeat          output lines can be repeated

Written by Arteen Abrishami
```
