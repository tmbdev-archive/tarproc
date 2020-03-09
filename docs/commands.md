
# Command `tsv2tar`

```
usage: Create a tar file for a csv/tsv plan. [-h] [-f DELIM] [-k KEY] [-C DIR] [-o OUTPUT] plan

positional arguments:
  plan

optional arguments:
  -h, --help            show this help message and exit
  -f DELIM, --delim DELIM
                        delimiter in csv/tsv file
  -k KEY, --key KEY     output format for record numbers
  -C DIR, --dir DIR     change into directory before executing
  -o OUTPUT, --output OUTPUT
                        output file (default: stdout)

The column headers contain the output filename extensions. Each column contains either data or a filename. Headers starting with "@" denote that the column contains actual file names. If there is a __key__
column, it is used as the key, otherwise records are numbered sequentially.

```
