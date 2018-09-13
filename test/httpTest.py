import http.client as client

#no proxy

# conn = client.HTTPConnection("docs.spring.io")
# conn.request("GET", '/spring/docs/5.0.8.RELEASE/spring-framework-reference/core.html#spring-core')
# data = conn.getresponse()
# print(data.read())


# use proxy
conn = client.HTTPSConnection("10.248.192.245:80")
conn.set_tunnel("docs.spring.io")
conn.request("GET", '/spring/docs/5.0.8.RELEASE/spring-framework-reference/')
data = conn.getresponse()
print(data.status)
print(data.read().decode('utf-8'))
conn.close()