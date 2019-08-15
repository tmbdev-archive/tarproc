# The Tarproc Utilities

For many big data applications, it is convenient to process data in record-sequential formats.
One of the most common such formats is `tar` archives.

We adopt the following conventions for record storage in tar archive:

- files are split into a key and a field name
- the key is the directory name plus the file name before the first dot
- the field name is the file name after the first dot
- files with the same key are grouped together and treated as a sample or record

This convention is followed both by these utilities as well as the `webdataset` `DataSet` implementation for PyTorch, available at http://github.com/tmbdev/webdataset

Here is an example of the ImageNet training data for deep learning:


```sos
tar tf testdata/imagenet-000000.tar | sed 5q
```

    10.cls
    10.png
    10.wnid
    10.xml
    12.cls
    tar: write error


The `tarshow` utility displays images and data from tar files; without the `-q` option, it will actually pop up an image window, but with `-q` it will simply display the records together.


```sos
tarshow < testdata/imagenet-000000.tar 2>&1 | sed 10q
```

    __key__             	10
    cls                 	b'304'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02X\x00\x00\x
    wnid                	b'n04380533'
    xml                 	b'None'
    
    __key__             	12
    cls                 	b'551'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x0
    wnid                	b'n03485407'


The `tarfirst` command outputs the first file matching some specification; this is useful for debugging.


```sos
tarfirst -s 3 -f wnid testdata/imagenet-000000.tar 
```

    18.wnid
    n02169497


```sos
tarfirst < testdata/imagenet-000000.tar > _test.image
file _test.image
```

    10.png
    _test.image: PNG image data, 600 x 793, 8-bit/color RGB, non-interlaced


We can actually search with an arbitrary Python expression; `_` is a dict with the field name as the key and the file contents as the value.


```sos
tarfirst -S 'int(_["cls"]) == 180' -f cls testdata/imagenet-000000.tar 
```

    13.cls
    180

# Creating Tar Shards

The `tarsplit` utility is useful for creating sharded tar files.


```sos
tarsplit -n 20 -o _test < testdata/sample.tar
```

    # writing _test-000000.tar (0, 0)
    # writing _test-000001.tar (20, 5880)
    # writing _test-000002.tar (40, 11233)
    # writing _test-000003.tar (60, 17020)
    # writing _test-000004.tar (80, 22757)


Commonly, we might use it with something more complex like this:


```sos
(cd /mdata/imagenet-raw/train && find . -name '*.JPEG' | tar -T - -cf -) | tarsplit --maxshards=5 -s 1e8 -o _test
```

    # writing _test-000000.tar (0, 0)
    # writing _test-000001.tar (803, 100051525)
    # writing _test-000002.tar (1520, 200122303)
    # writing _test-000003.tar (2113, 300254739)
    # writing _test-000004.tar (2778, 400408574)
    tar: -: Wrote only 6144 of 10240 bytes
    tar: Error is not recoverable: exiting now
    find: ‘standard output’: Broken pipe
    find: write error


# Concatenating Tar Files

You can reshard with a combination of `tarcat` and `tarsplit` (here we're using the same tar file as input multiple times, but in practice, you'd of course use separate shards).


```sos
tarcat testdata/sample.tar testdata/sample.tar | tarsplit -n 60
```

    # got 2 files
    # 0 testdata/sample.tar
    # writing temp-000000.tar (0, 0)
    # writing temp-000001.tar (60, 17020)
    # 90 testdata/sample.tar
    # writing temp-000002.tar (120, 34157)


The `tarcat` utility also lets you specify a downloader command (for accessing object stores) and can expand shard syntax. Here is a more complex example:


```sos
tarcat -c 'gsutil cat {}' -b 'gs://lpr-imagenet/imagenet_train-{0000..0147}.tgz' | tar2tsv -f cls | sed 10q
```

    # got 148 files
    # 0 gs://lpr-imagenet/imagenet_train-0000.tgz


    Keyboard Interrupt


# Creating Tar Files from TSV Files

You can create `tar` archives from TSV files. The first line is a header that gives the field names, subsequent lines are data. Headers starting with "@" cause the corresponding field content to be interpreted as a file name that gets incorporated by binary-reading it.

Of course, this too combines with `tarsplit` and other utilities.


```sos
sed 3q testdata/plan.tsv
```

    @file	a	b	c
    hello	1	1	1
    hello	1	1	1



```sos
tarcreate -C testdata testdata/plan.tsv | tar tvf - | sed 10q
```

    ['@file', 'a', 'b', 'c']
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000000.a
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000000.b
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000000.c
    -r--r--r-- bigdata/bigdata   6 2019-08-15 09:04 000000000.file
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000001.a
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000001.b
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000001.c
    -r--r--r-- bigdata/bigdata   6 2019-08-15 09:04 000000001.file
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000002.a
    -r--r--r-- bigdata/bigdata   1 2019-08-15 09:04 000000002.b
    tar: write error


# Sorting

You can sort the records (grouped files) in a `tar` archive using `tarsort`.

You can use any content for sorting. Here, we sort on the content of the `cls` field, interpreting it as an `int`.


```sos
tarsort --sortkey cls --sorttype int --update < testdata/imagenet-000000.tar > _sorted.tar
```


```sos
tar2tsv -s 5 -f "cls wnid" testdata/imagenet-000000.tar
echo
tar2tsv -s 5 -f "cls wnid" _sorted.tar
```

    10	304	n04380533
    12	551	n03485407
    13	180	n02088632
    15	165	n02410509
    18	625	n02169497
    
    27	897	n03220513
    63	439	n02051845
    59	75	n02500267
    69	55	n02123159
    43	966	n03188531


You can also use `tarsort` for shuffling records.


```sos
tarsort --sorttype shuffle < testdata/imagenet-000000.tar > _sorted.tar
tar2tsv -s 5 -f "cls wnid" _sorted.tar
```

    27	897	n03220513
    63	439	n02051845
    59	75	n02500267
    69	55	n02123159
    43	966	n03188531


# Mapping / Parallel Processing

The `tarproc` utility lets you map command line programs and scripts over the samples in a tar file.


```sos
time tarproc -c "gm mogrify -size 256x256 *.png" < testdata/imagenet-000000.tar > _out.tar
```

    
    real	0m3.987s
    user	0m3.673s
    sys	0m0.307s


You can even parallelize this (somewhat analogous to `xargs`):


```sos
time tarproc -p 8 -c "gm mogrify -size 256x256 *.png" < testdata/imagenet-000000.tar > _out.tar
```

    
    real	0m0.801s
    user	0m4.208s
    sys	0m0.359s



```sos

```
