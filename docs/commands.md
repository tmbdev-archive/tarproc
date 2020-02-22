Usage information for command line programs.
# tar2tsv (command)

```
usage: Extract textual information from tar training files. [-h] [-f FIELDS] [-c COUNT] [--nokey] [--noheader] [input]

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -f FIELDS, --fields FIELDS
                        fields
  -c COUNT, --count COUNT
                        maximum number of output records
  --nokey               don't output the key field
  --noheader            don't output a header
```

# tarcats (command)

```
usage: Concatenate tar files sequentially to standard out. [-h] [-v] [-T FILELIST] [-b] [-s SKIP] [-c COUNT] [-o OUTPUT]
                                                           [--output-mode OUTPUT_MODE] [--shuffle SHUFFLE] [--eof] [--nodata]
                                                           [input [input ...]]

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -T FILELIST, --filelist FILELIST
  -b, --braceexpand
  -s SKIP, --skip SKIP
  -c COUNT, --count COUNT
  -o OUTPUT, --output OUTPUT
  --output-mode OUTPUT_MODE
  --shuffle SHUFFLE
  --eof
  --nodata
```

# tarfirst (command)

```
usage: Dump the first matching file from a tar file. [-h] [-S SELECT] [-v] [-f FIELD] [input]

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -S SELECT, --select SELECT
                        expression that must evaluate to true before saving
  -v, --verbose         output more information
  -f FIELD, --field FIELD
                        field to be selected
```

# tarmix (command)

```
usage: tarmix [-h] [-v] [-c COUNT] [-o OUTPUT] [--output-mode OUTPUT_MODE] [--skip SKIP] [--shuffle SHUFFLE] [--eof] yamlspec

Randomly mix data sources to standard out.

positional arguments:
  yamlspec

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -c COUNT, --count COUNT
  -o OUTPUT, --output OUTPUT
  --output-mode OUTPUT_MODE
  --skip SKIP
  --shuffle SHUFFLE
  --eof

The mix is specified by a YAML file that looks something like this:

```YAML
    shuffle: 1000
    sources:
      - shards: "gs://bucket1/data-{000..999}.tar"
        weight: 1
        probability: 0.9
        shuffle: 10000
      - shards: "gs://bucket3/data-{000..100}.tar"
        weight: 1.7
        probability: 0.5
        nstreams: 10
        nrepeats: 5
        convert:
          - from: page.jpg
            to: png
```

The source attributes have the following meaning:

    - shards: actual shard spec
    - weight: streams are chosen for sampling with a probability proportional to weight
    - probability: samples are output from a stream with this probability
    - nstreams: for multi-sharded streams, tries to keep this many streams open in parallel
    - nrepeats: repeats the source this often
    - convert: perform a limited number of sample format conversions
    - rename: rename sample components (rename to "" to delete)
    - shuffle: shuffle the files and samples for this stream
    - allow_missing: permit input files to be missing for the stream

Global parameters:

    - shuffle: shuffle the output samples before writing (use external program for very large shuffles)
```

# tarpcat (command)

```
usage: tarpcat [-h] [-v] [-T FILELIST] [-b] [-c COUNT] [-s SHUFFLE] [-p WORKERS] [-o OUTPUT] [--dummy] [input [input ...]]

Read, shuffle, and combine multiple shards in parallel.

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -T FILELIST, --filelist FILELIST
  -b, --braceexpand
  -c COUNT, --count COUNT
  -s SHUFFLE, --shuffle SHUFFLE
  -p WORKERS, --workers WORKERS
  -o OUTPUT, --output OUTPUT
  --dummy
```

# tarproc (command)

```
usage: tarproc [-h] [-v] [-q] [-c COMMAND] [-S SCRIPT] [-w WORKING_DIR] [-b BASE] [-f FIELDS] [-F FIELDMODE] [-p PARALLEL]
               [-e ERROR_HANDLING] [-E EXCLUDE] [-I INCLUDE] [-s SEPARATOR] [--interpreter INTERPRETER] [--count COUNT] [-o OUTPUT]
               [input]

Run commands over all samples.

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         output extra information
  -q, --silent          extra quiet
  -c COMMAND, --command COMMAND
                        command to run for each sample (working dir = sample)
  -S SCRIPT, --script SCRIPT
                        script to run for each sample (working dir = sample)
  -w WORKING_DIR, --working_dir WORKING_DIR
                        temporary working dir
  -b BASE, --base BASE  base to substitute for __key__ (default="sample")
  -f FIELDS, --fields FIELDS
                        fields to run on (default=all, space separated)
  -F FIELDMODE, --fieldmode FIELDMODE
                        how to handle missing fields (error or ignore)
  -p PARALLEL, --parallel PARALLEL
                        execute scripts in parallel
  -e ERROR_HANDLING, --error-handling ERROR_HANDLING
                        how to handle errors in scripts (ignore, skip, abort)
  -E EXCLUDE, --exclude EXCLUDE
                        exclude anything matching this from output
  -I INCLUDE, --include INCLUDE
                        include only files matching this in output
  -s SEPARATOR, --separator SEPARATOR
                        separator between key and new file bases
  --interpreter INTERPRETER
                        interpreter used for script argument
  --count COUNT         stop after processing this many samples
  -o OUTPUT, --output OUTPUT

Run a command line tool over all samples.

Each sample is extracted into its own directory with
a common basename (default=sample) and the extensions from the sample.

Example:

    tarproc -I png -c 'convert sample.jpg sample.png' inputs.tar -o outputs.tar
```

# tarshow (command)

```
usage: Show data inside a tar file. [-h] [-f FIELD] [-c COUNT] [-N] [-C CMAP] [-d DELAY] [--silent] [--verbatim-keys] [--use-keyboard]
                                    [input]

positional arguments:
  input                 tar file

optional arguments:
  -h, --help            show this help message and exit
  -f FIELD, --field FIELD
                        field to be viewed
  -c COUNT, --count COUNT
                        number of records to display
  -N, --normalize       normalize images before display
  -C CMAP, --cmap CMAP  color map for images
  -d DELAY, --delay DELAY
                        delay between displayed images records
  --silent              less output
  --verbatim-keys       compare keys verbatim (rather than case sensitive)
  --use-keyboard        use the keyboard rather than the mouse for input
```

# tarsort (command)

```
usage: Sort the samples inside a tar file. [-h] [-k KEY] [-s SORTKEY] [-S SORTTYPE] [-r REPORT] [-t TEMPFILE] [-o OUTPUT] [--update]
                                           [--keep] [--commit COMMIT]
                                           [input]

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY
  -s SORTKEY, --sortkey SORTKEY
  -S SORTTYPE, --sorttype SORTTYPE
  -r REPORT, --report REPORT
  -t TEMPFILE, --tempfile TEMPFILE
  -o OUTPUT, --output OUTPUT
  --update
  --keep
  --commit COMMIT
```

# tarsplit (command)

```
usage: Split a tar file into shards based on size or number of samples. [-h] [-n NUM_SAMPLES] [-s MAX_SIZE] [-v] [-C COMMAND] [-o OUTPUT]
                                                                        [-O OPEN] [-z] [--start START] [--maxshards MAXSHARDS]
                                                                        [--nodelete]
                                                                        [input]

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SAMPLES, --num-samples NUM_SAMPLES
  -s MAX_SIZE, --max-size MAX_SIZE
  -v, --verbose
  -C COMMAND, --command COMMAND
  -o OUTPUT, --output OUTPUT
  -O OPEN, --open OPEN
  -z, --compress
  --start START
  --maxshards MAXSHARDS
  --nodelete            don't delete after executing command
```

# tsv2tar (command)

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

The column headers contain the output filename extensions. Each column contains either data or a filename. Headers starting with "@"
denote that the column contains actual file names. If there is a __key__ column, it is used as the key, otherwise records are numbered
sequentially.
```

