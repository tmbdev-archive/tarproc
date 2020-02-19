# tarproclib.zcom

## zmq_make
```python
zmq_make(context, url, linger=0)
```
Make a ZMQ socket for a context and url.

- context: context
- url: target URL
- linger: linger flag

## zmq_connect
```python
zmq_connect(socket, urls, topic='')
```
Explicitly connect to a ZMQ socket.

- url: ZMQ-URL to connect to  (Default value = "")
- topic: topic to subscribe to for SUB sockets (Default value = "")


## Connection
```python
Connection(self, urls=None, noexpand=False, keep_meta=True, **kw)
```
A class for sending/receiving samples via ZMQ sockets.
## MultiWriter
```python
MultiWriter(self, urls=None, noexpand=False, keep_meta=True, linger=-1, output_mode='random', **kw)
```
A class for sending/receiving samples via ZMQ sockets.
