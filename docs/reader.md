# tarproclib.reader

## tariterator
```python
tariterator(fileobj, keys=<function base_plus_ext at 0x7ff171d75dd0>, decoder=None, suffixes=None, errors=True, container=None)
```
Iterate through training samples stored in a sharded tar file.

- fileobj:
- check_sorted:  (Default value = False)
- keys:  (Default value = base_plus_ext)
- decode:  (Default value = True)


## TarIterator1
```python
TarIterator1(self, url, braceexpand=True, shuffle=False, allow_missing=False, **kw)
```
Iterate of tar files consisting of samples.

- url: source URL
- braceexpand: expand braces in the source URL
- shuffle: shuffle the samples
- allow_missing: allow missing shards
- **kw:

## TarIterator
```python
TarIterator(url, **kw)
```
Open an iterator of tar files.

This can open either ZMQ URLs or object store URLs.

- url: source URL
- **kw:

