import unittest
import multiprocessing as mp
import numpy as np
import os

from sklearn import svm
from mlsocket import MLSocket
from importlib.util import find_spec


TEST_KERAS = False

if find_spec('tensorflow'):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    from tensorflow.keras.models import load_model
    TEST_KERAS = True


class Client_Process(mp.Process):

    def __init__(self, host, port, data):
        self.data = data
        self.host = host
        self.port = port
        super().__init__()

    def run(self):
        if self.data == 'keras':
            self.data = load_model(f'{os.path.dirname(__file__)}/weights.h5')
        with MLSocket() as s:
            print(f"Client socket opening with host: {self.host} and "
                  f"port: {self.port}")
            s.connect((self.host, self.port))
            print(f"Client sending {self.data}")
            s.send(self.data)


def open_client_process(host, port, data):
    client_process = Client_Process(host, port, data)
    client_process.daemon = True
    client_process.start()


class TestMLSocket(unittest.TestCase):
    """Tests for 'MLSocket' class"""

    def setUp(self) -> None:
        self.HOST = '127.0.0.1'
        self.PORT = np.random.randint(0, 65535)

    def test_bytes(self):
        """Test for sending byte data through localhost"""
        send_data = b'Hello World'
        print(f"\nServer opening at {self.HOST}")
        open_client_process(self.HOST, self.PORT, send_data)
        with MLSocket() as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, address = s.accept()
            print(f"Client accepted with {address}")
            with conn:
                recv_data = conn.recv(1024)
                print(f"Server received {recv_data}")
                self.assertEqual(recv_data, send_data)

    def test_numpy(self):
        """Test for sending numpy through localhost"""
        send_data = np.array([1, 2, 3, 4])
        print(f"\nServer opening at {self.HOST}")
        open_client_process(self.HOST, self.PORT, send_data)
        with MLSocket() as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, address = s.accept()
            print(f"Client accepted with {address}")
            with conn:
                recv_data = conn.recv(1024)
                print(f"Server received {recv_data}")
                self.assertEqual(recv_data.shape, send_data.shape)
                for i in range(send_data.shape[0]):
                    self.assertEqual(
                        send_data[i], recv_data[i]
                    )

    def test_scikit_learn(self):
        """Test for sending scikit-learn model through localhost"""
        expected_gamma = 0.031415
        send_data = svm.SVC(gamma=expected_gamma)
        print(f"\nServer opening at {self.HOST}")
        open_client_process(self.HOST, self.PORT, send_data)
        with MLSocket() as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, address = s.accept()
            print(f"Client accepted with {address}")
            with conn:
                recv_data = conn.recv(1024)
                print(f"Server received {recv_data}")
                self.assertEqual(type(recv_data), type(send_data))
                self.assertEqual(recv_data.gamma, expected_gamma)

    def test_keras_model(self):
        """Test for sending keras model through localhost"""
        if not TEST_KERAS:
            print("Skipping keras test because no tensorflow module is found")
            return
        model = load_model(f'{os.path.dirname(__file__)}/weights.h5')
        data = np.ones(4).reshape((1, 4))
        o_result = model.predict(data)[0][0]
        print(f"Original prediction result: {o_result}")
        print(f"\nServer opening at {self.HOST}")
        open_client_process(self.HOST, self.PORT, 'keras')
        with MLSocket() as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, address = s.accept()
            print(f"Client accepted with {address}")
            with conn:
                recv_model = conn.recv(1024)
                r_result = recv_model.predict(data)[0][0]
                print(f"Server received {recv_model}")
                print(f"Received prediction result:"
                      f" {r_result}")
                self.assertEqual(o_result, r_result)
                self.assertEqual(len(recv_model.layers), len(model.layers))


if __name__ == "__main__":
    unittest.main()
