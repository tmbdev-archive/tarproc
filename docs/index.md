# The Tarproc Utilities

For many big data applications, it is convenient to process data in record-sequential formats.
One of the most common such formats is `tar` archives.

All we really need for sequential data processing is that files that need to be processed together
are adjacent in a `tar` file and that we can group together files into records.
The convention that the `tarproc` utilities follow is that the entire path up to the first dot ('.')
in the filename constitutes the file prefix, and that all files with the same prefix are treated
as part of the same record. For many datasets, files in this format can simply be generated
with `tar --sorted=name cf data.tar ...`.

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


The `tarshow` utility displays images and data from tar files.


```sos
tarshow -d 0 'testdata/imagenet-000000.tar#0,3'
```

    __key__             	10
    __source__          	testdata/imagenet-000000.tar
    cls                 	b'304'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x02X\x00\x00\x
    wnid                	b'n04380533'
    xml                 	b'None'
    
    __key__             	12
    __source__          	testdata/imagenet-000000.tar
    cls                 	b'551'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xc8\x00\x0
    wnid                	b'n03485407'
    xml                 	b'None'
    
    __key__             	13
    __source__          	testdata/imagenet-000000.tar
    cls                 	b'180'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90\x00\x0
    wnid                	b'n02088632'
    xml                 	b'None'
    
    __key__             	15
    __source__          	testdata/imagenet-000000.tar
    cls                 	b'165'
    png                 	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\xf4\x00\x0
    wnid                	b'n02410509'
    xml                 	b'<annotation>\n\t<folder>n02410509</folder>\n\t<filename>n0
    


The `tarfirst` command outputs the first file matching some specification; this is useful for debugging.


```sos
tarfirst -f wnid testdata/imagenet-000000.tar
```

    10.wnid
    n04380533


```sos
tarfirst testdata/imagenet-000000.tar > _test.image
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
tarsplit -n 20 -o _test testdata/sample.tar
```

    # writing _test-000000.tar (0, 0)
    # writing _test-000001.tar (20, 6460)
    # writing _test-000002.tar (40, 12393)
    # writing _test-000003.tar (60, 18760)
    # writing _test-000004.tar (80, 25077)


Commonly, we might use it with something more complex like this:


```sos
(cd /mdata/imagenet-raw/train && find . -name '*.JPEG' | tar -T - -cf -) | tarsplit --maxshards=5 -s 1e8 -o _test
```

    # writing _test-000000.tar (0, 0)
    # writing _test-000001.tar (803, 100060358)
    # writing _test-000002.tar (1520, 200139023)
    # writing _test-000003.tar (2113, 300277982)
    # writing _test-000004.tar (2777, 400283020)
    tar: -: Wrote only 4096 of 10240 bytes
    tar: Error is not recoverable: exiting now


    Keyboard Interrupt


# Concatenating Tar Files

You can reshard with a combination of `tarcat` and `tarsplit` (here we're using the same tar file as input multiple times, but in practice, you'd of course use separate shards).


```sos
tarscat testdata/sample.tar testdata/sample.tar | tarsplit -n 60
```

    # got 2 files
    # 0 testdata/sample.tar
    # writing temp-000000.tar (0, 0)
    # writing temp-000001.tar (60, 18760)
    # 90 testdata/sample.tar
    # writing temp-000002.tar (120, 37637)


The `tarcats` utility also lets you specify a downloader command (for accessing object stores) and can expand shard syntax. Here is a more complex example. Downloader commands are specified by setting environment variables for each URL schema.


```sos
export GOPEN_GS="gsutil cat '{}'"
export GOPEN_HTTP="curl --silent -L '{}'"
```


```sos
tarcats -c 10 'gs://lpr-imagenet/imagenet_train-0000.tgz' | tar2tsv -f cls
```

    # got 1 files
    # 0 gs://lpr-imagenet/imagenet_train-0000.tgz
    __key__	cls
    n03788365_17158	852
    n03000247_49831	902
    n03000247_22907	902
    n04597913_10741	951
    n02117135_412	34
    n03977966_79041	285
    n04162706_8032	589
    n03670208_11267	270
    n02782093_1594	233
    n02172182_3093	626



```sos
tarcats --shuffle -c 3 -b 'gs://lpr-imagenet/imagenet_train-{0000..0147}.tgz' > _temp.tar
```

    # got 148 files
    # 0 gs://lpr-imagenet/imagenet_train-0043.tgz



```sos
tarshow -d 0 _temp.tar
```

    __key__             	n07753113_21272
    __source__          	b'gs://lpr-imagenet/imagenet_train-0043.tgz'
    cls                 	b'321'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00
    json                	b'{"cls": 321, "cname": "fig"}'
    
    __key__             	n02408429_6603
    __source__          	b'gs://lpr-imagenet/imagenet_train-0043.tgz'
    cls                 	b'162'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00
    json                	b'{"cls": 162, "cname": "water buffalo, water ox, Asiatic bu
    
    __key__             	n03485794_6421
    __source__          	b'gs://lpr-imagenet/imagenet_train-0043.tgz'
    cls                 	b'750'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00
    json                	b'{"cls": 750, "cname": "handkerchief, hankie, hanky, hankey
    



```sos
tarshow -d 0 'gs://lpr-imagenet/imagenet_train-{0000..0099}.tgz#0,3'
```

    __key__             	n03788365_17158
    __source__          	gs://lpr-imagenet/imagenet_train-0000.tgz
    cls                 	b'852'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x0e\xd8\x0e\x
    json                	b'{"annotation": {"folder": "n03788365", "filename": "n03788
    
    __key__             	n03000247_49831
    __source__          	gs://lpr-imagenet/imagenet_train-0000.tgz
    cls                 	b'902'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\xf0\x00\x
    json                	b'{"cls": 902, "cname": "chain mail, ring mail, mail, chain 
    
    __key__             	n03000247_22907
    __source__          	gs://lpr-imagenet/imagenet_train-0000.tgz
    cls                 	b'902'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00
    json                	b'{"annotation": {"folder": "n03000247", "filename": "n03000
    
    __key__             	n04597913_10741
    __source__          	gs://lpr-imagenet/imagenet_train-0000.tgz
    cls                 	b'951'
    jpg                 	b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\xfa\x00\x
    json                	b'{"annotation": {"folder": "n04597913", "filename": "n04597
    


# Creating Tar Files from TSV Files

You can create `tar` archives from TSV files. The first line is a header that gives the field names, subsequent lines are data. Headers starting with "@" cause the corresponding field content to be interpreted as a file name that gets incorporated by binary-reading it.

Of course, this too combines with `tarsplit` and other utilities.


```sos
sed 3q testdata/plan.tsv
```

    __key__	@file	a	b	c
    a	hello	1	1	1
    b	hello	1	1	1



```sos
tarcreate -C testdata testdata/plan.tsv | tarshow -c 3
```

    ['__key__', '@file', 'a', 'b', 'c']
    __key__             	a
    __source__          	-
    a                   	b'1'
    b                   	b'1'
    c                   	b'1'
    file                	b'world\n'
    
    __key__             	b
    __source__          	-
    a                   	b'1'
    b                   	b'1'
    c                   	b'1'
    file                	b'world\n'
    
    __key__             	c
    __source__          	-
    a                   	b'1'
    b                   	b'1'
    c                   	b'f'
    


# Sorting

You can sort the records (grouped files) in a `tar` archive using `tarsort`.

You can use any content for sorting. Here, we sort on the content of the `cls` field, interpreting it as an `int`.


```sos
tarsort --sortkey cls --sorttype int --update testdata/imagenet-000000.tar > _sorted.tar
```


```sos
tar2tsv -c 5 -f "cls wnid" testdata/imagenet-000000.tar
echo
tar2tsv -c 5 -f "cls wnid" _sorted.tar
```

    __key__	cls	wnid
    10	304	n04380533
    12	551	n03485407
    13	180	n02088632
    15	165	n02410509
    18	625	n02169497
    
    __key__	cls	wnid
    77	14	n02077923
    75	25	n02092339
    46	27	n02096437
    80	53	n02356798
    29	54	n02488702


You can also use `tarsort` for shuffling records.


```sos
tarsort --sorttype shuffle < testdata/imagenet-000000.tar > _sorted.tar
tar2tsv -c 5 -f "cls wnid" _sorted.tar
```

    __key__	cls	wnid
    27	897	n03220513
    63	439	n02051845
    59	75	n02500267
    69	55	n02123159
    43	966	n03188531


# Mapping / Parallel Processing

The `tarproc` utility lets you map command line programs and scripts over the samples in a tar file.


```sos
time tarproc -c "gm mogrify -size 256x256 *.png" < testdata/imagenet-000000.tar -o - > _out.tar
```

    
    real	0m3.866s
    user	0m3.520s
    sys	0m0.332s


You can even parallelize this (somewhat analogous to `xargs`):


```sos
time tarproc -p 8 -c "gm mogrify -size 256x256 *.png" < testdata/imagenet-000000.tar -o - > _out.tar
```

    
    real	0m0.804s
    user	0m4.190s
    sys	0m0.389s


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

