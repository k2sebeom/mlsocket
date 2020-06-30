from mlsocket import MLSocket

HOST = '127.0.0.1'
PORT = 65432

with MLSocket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, address = s.accept()

    with conn:
        data = conn.recv(1024)
        model = conn.recv(1024)
        clf = conn.recv(1024)