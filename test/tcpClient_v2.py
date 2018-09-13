import socket

# file path for output.
fname='C:/manual/hibernate_jpa2.html'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip is always 10.248.192.245, cause this is proxy server.
s.connect(("10.248.192.245", 80))
http = b'GET /hibernate/orm/5.3/userguide/html_single/Hibernate_User_Guide.html HTTP/1.1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nHost: docs.jboss.org\r\n\r\n'
s.send(http)



sf=s.makefile("rb")

headers = []
total = 0
while True:
    line = sf.readline()
    headers.append(line)
    if line in (b'\r\n', b'\n', b''):
        break
hstring = b''.join(headers).decode('utf-8')
print(hstring)
print("---")

headerstr=hstring.split('\r\n')
for h in headerstr:
    if h.startswith('Content-Length:'):
        # total = int(h[len('Content-Length: '):]) - len(hstring)
        total = int(h[len('Content-Length: '):])
        break

print(total)

bodys = []
MAXAMOUNT = 1048576
while total > 0:
    body = sf.read(min(total, MAXAMOUNT))
    if not body:
        raise Exception
    bodys.append(body)
    total -= len(body)

s.close()

f = open(fname, 'wb')

if len(bodys) > 0:
    # print(b''.join(bodys).decode('utf-8'))
    f.write(b''.join(bodys))
f.close()
