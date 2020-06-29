import os
import socket
import numpy as np
import h5py

from io import BytesIO
from joblib import dump, load
from socket import getdefaulttimeout
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model, save_model


class MLSocket(socket.socket):
    def __init__(self, proto=-1, fileno=None):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM, proto, fileno)

    def accept(self):
        fd, addr = super()._accept()
        sock = MLSocket(proto=self.proto, fileno=fd)

        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __parse_data(data):
        buffer = BytesIO()
        if isinstance(data, np.ndarray):
            np.save(buffer, data, allow_pickle=True)
        elif 'keras' in str(type(data)):
            with h5py.File(buffer, 'w') as f:
                save_model(data, f, include_optimizer=True)
        elif 'sklearn' in str(type(data)):
            dump(data, buffer)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def __load_data(file: BytesIO):
        data = file.read()
        file.seek(0)
        if b'NUMPY' in data:
            return np.load(file)
        elif b'sklearn' in data:
            return load(file)
        elif b'HDF' in data:
            with h5py.File(file, 'r') as f:
                model = load_model(f)
            return model

    def sendall(self, data: bytes, flags: int = ...) -> None:
        data = self.__parse_data(data)
        super().sendall(data)
        super().sendall(b'End')
        super().recv(1024)

    def send(self, data: bytes, flags: int = ...) -> int:
        data = self.__parse_data(data)
        result = super().send(data)
        super().send(b'End')
        super().recv(1024)
        return result

    def recv(self, bufsize: int, flags: int = ...) -> bytes:
        buffer = BytesIO()
        while True:
            data = super().recv(bufsize)
            if not data:
                break
            buffer.write(data)
            buffer.seek(-4, 2)
            if b'End' in buffer.read():
                super().send(b'Complete')
                break
        buffer.seek(0)
        return self.__load_data(buffer)
