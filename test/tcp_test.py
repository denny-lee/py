import socket

fname='C:/Users/e657183/Desktop/test1.txt'
f = open(fname, 'rb')
# file path for output.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip is always 10.248.192.245, cause this is proxy server.
s.connect(("localhost", 8080))
if f:
    http=f.read()
f.close()

s.send(http)

chunks = []
bytes_recd = 0
total = 0
idx=0

while True:
    chunk = s.recv(128)
    if chunk != b'':
        chunks.append(chunk)
    if len(chunk) > 2 and '\r\n\r\n' in b''.join(chunks).decode('utf-8'):
        break

h = b''.join(chunks).decode('ISO-8859-1')
print(h)
idx = h.index('\r\n\r\n')
headers=h.split('\r\n')
for h in headers:
    if h.startswith('Content-Length:'):
        total = int(h[len('Content-Length: '):])
        break

while bytes_recd  < total:
    chunk = s.recv(min(total - bytes_recd, 2048))
    if chunk == b'':
        raise Exception('empty')
    chunks.append(chunk)
    bytes_recd = bytes_recd + len(chunk)

print(b''.join(chunks)[idx+4:].decode('ISO-8859-1'))


s.close()