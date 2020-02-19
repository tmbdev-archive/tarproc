# tarproclib.reader

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

