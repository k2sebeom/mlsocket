# mlsocket
MLSocket is a python package built on top of the python package of socket to easily send and receive numpy arrays and machine learning models through tcp connection.

* Free software: MIT license

MLSocket class inherits a built-in socket package of python and supports all of the basic operations of the socket class.
It can not only send the byte data but also send numpy arrays and keras models.

------

## Installation

    $ pip install mlsocket --user
    

## Features

* Supports Windows 10, Ubuntu, and macOs => Tested on github action
* Supports data transfer of numpy arrays
* Supports data transfer of keras models as hdf5 files
* Supports data transfer of scikit-learn classifiers
* Support python 3.6, 3.6, 3.8 => Tested on github action

MLSocket inherits the socket object of the built-in python socket, but overrides 4 methods.

* MLSocket.send(data), MLSocket.sendall(data): Sends the data. Unlike socket.send, thses two functions always show blocking behavior that it waits for the reponse from the server that the server received all the data sent.
* MLSocket.recv(bufsize): Receives data of the given size, but the return value is not in the size of bufsize. It will receive all the data sent by the client, with the step size of a given bufsize.
* MLSocket.accept(): This function is just the same as socket.accept(), but returns the MLSocket object and the connected address.

## Usage

The basic usage of the MLSocket is demonstrated by the following scripts of server and client which sends and receives numpy array and machine learning models.

#### Server-Side

```python
from mlsocket import MLSocket

HOST = '127.0.0.1'
PORT = 65432

with MLSocket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, address = s.accept()

    with conn:
        data = conn.recv(1024) # This will block until it receives all the data send by the client, with the step size of 1024 bytes.
        model = conn.recv(1024) # This will also block until it receives all the data.
        clf = conn.recv(1024) # Same
```

#### Client-Side
```python
from mlsocket import MLSocket
from keras.models import Sequential
from keras.layers import Dense
from sklearn import svm
import numpy as np

HOST = '127.0.0.1'
PORT = 65432

# Make an ndarray
data = np.array([1, 2, 3, 4])

# Make a keras model
model = Sequential()
model.add(Dense(8, input_shape=(None, 4)))
model.compile(optimizer='adam', loss='binary_crossentropy')

# Make a scikit-learn classifier
clf = svm.SVC(gamma=0.00314)

# Send data
with MLSocket() as s:
    s.connect((HOST, PORT)) # Connect to the port and host
    s.send(data) # After sending the data, it will wait until it receives the reponse from the server
    s.send(model) # This will wait as well
    s.send(clf) # Same
```
    
