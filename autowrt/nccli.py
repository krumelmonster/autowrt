import time
import io
from socket import socket


def mayrecv(sock):
    try:
        msg = sock.recv(512)
    except OSError:
        msg = None
    return msg


class Multiwriter:
    def __init__(self, textwriters=[], binarywriters=[]):
        self.textwriters = textwriters
        self.binarywriters=binarywriters

    def write(self, bytes):
        for textwriter in self.textwriters:
            textwriter.write(bytes.decode('utf-8'))
        for binarywriter in self.binarywriters:
            binarywriter.write(bytes)

class NcCli:
    sock: socket

    def __init__(self, sock: socket):
        self.sock = sock
        self.buffer = bytearray(b'')
        self.lastwrite=0

        self.sock.settimeout(0.05)
        # self.run('PS1='+self.delimiter+'; echo PS1set\n')
        # print(self.result())

    def run(self, cmd: str):
        self.sock.sendall(bytes(cmd+"\n", 'ascii'))

    def bresult(self, delimiter: str):
        data = io.BytesIO()
        self.write_result(data, delimiter)
        return data.getvalue()

    def result(self, delimiter: str) -> str:
        return self.bresult(delimiter).decode('utf-8')

    def write_result(self, stream, delimiter: str) -> None:
        bdelimiter = delimiter.encode('ascii')
        fresh = True
        self.lastwrite=0
        while True:
            pkg = mayrecv(self.sock)
            if pkg or fresh:
                fresh = False
                # print(buf.decode('utf-8'))
                # print('.')
                if pkg:
                    self.buffer.extend(pkg)
                found = self.buffer.find(bdelimiter)
                if found > -1:
                    # print(':'+str(found)+':')
                    stream.write(self.buffer[:found])
                    self.lastwrite+=found
                    self.buffer = self.buffer[found + len(bdelimiter):]
                    return
                else:
                    done = max(len(self.buffer) - len(bdelimiter), 0)
                    stream.write(self.buffer[:done])
                    self.lastwrite+=done
                    self.buffer = self.buffer[done:]
            else:
                time.sleep(0.1)
