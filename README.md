[![Test](https://github.com/tmbdev/tarproc/workflows/Test/badge.svg)](https://github.com/tmbdev/tarproc/actions?query=workflow%3ATest)
[![TestPip](https://github.com/tmbdev/tarproc/workflows/TestPip/badge.svg)](https://github.com/tmbdev/tarproc/actions?query=workflow%3ATestPip)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/tmbdev/tarproc/?ref=repository-badge)

# The Tarproc Utilities

Tarfiles are commonly used for storing large amounts of data in an efficient,
sequential access, compressed file format, in particualr for deep learning
applications. For processing and data transformation,
people usually unpack them, operate over the files, and tar up the result again.

This library and set of utilities permits operating directly on tar files. This
is faster than operating on files on file systems, and it is usually easier too.

- tarcats -- concatenate tar files sequentially
- tarsplit -- split a tar file by number of records or size
- tarpcat -- concatenate tar files in parallel
- tarproc -- map command line programs over tar files
- tarshow -- show contents of tar files
- tarsort -- sort tar files based on some key

The following are less commonly used utilities that are specifically useful
for deep learning:

- tarfirst -- extract the first file matching some criteria
- targrep -- grep through files inside tar files (this will replace tarfirst)
- tar2db, tar2lmdb, tar2tsv -- convert tar files to database files
- tarmix -- mix tar files based on statistical sampling
- tsv2tar -- build tar files based on a .tsv file plan

The utilities allow operating on stdin/stdout when necessary, allowing
command line pipes to be constructed. For example:

```Bash
    $ gsutil cat gs://bucket/file.tar | tarsort | tarsplit -o output
```

# Python Interface


```sos
from tarproclib import reader, gopen
from itertools import islice

gopen.handlers["gs"] = "gsutil cat '{}'"

for sample in islice(reader.TarIterator("gs://lpr-imagenet/imagenet_train-0000.tgz"), 0, 10):
    print(sample.keys())
```

    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])
    dict_keys(['__key__', 'cls', 'jpg', 'json', '__source__'])

