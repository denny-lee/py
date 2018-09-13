import socket

# file path for output.
fname='C:/mission/hibernate_jpa.html'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip is always 10.248.192.245, cause this is proxy server.
s.connect(("10.248.192.245", 80))
http = b'GET /hibernate/orm/5.3/userguide/html_single/Hibernate_User_Guide.html HTTP/1.1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nHost: docs.jboss.org\r\n\r\n'
s.send(http)

chunks = []
bytes_recd = 0
total = 0
idx=0

while True:
    chunk = s.recv(512)
    if chunk != b'':
        chunks.append(chunk)
    if len(chunk) > 2 and '\r\n\r\n' in b''.join(chunks).decode('utf-8'):
        break

h = b''.join(chunks).decode('utf-8')
idx = h.index('\r\n\r\n')
headers=h.split('\r\n')
for h in headers:
    if h.startswith('Content-Length:'):
        total = int(h[len('Content-Length: '):])
        break



while bytes_recd +idx+4 < total:
    chunk = s.recv(min(total - bytes_recd, 2048))
    if chunk == b'':
        raise Exception('empty')
    chunks.append(chunk)
    bytes_recd = bytes_recd + len(chunk)

s.close()

f = open(fname, 'wb')

if len(chunks) > 0:
    # print(b''.join(chunks).decode('utf-8'))
    f.write(b''.join(chunks)[idx+4:])
f.close()
