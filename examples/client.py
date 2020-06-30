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
    s.send(data)
    s.send(model)
    s.send(clf)
