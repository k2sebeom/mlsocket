import unittest
from mlsocket import MLSocket
import multiprocessing as mp
from sklearn import svm
import numpy as np


class Client_Process(mp.Process):

    def __init__(self, host, port, data):
        super().__init__()
        self.data = data
        self.host = host
        self.port = port

    def run(self):
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


if __name__ == "__main__":
    unittest.main()
