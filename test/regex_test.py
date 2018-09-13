import re

f = open('C:/Users/e657183/Desktop/ttt.txt', 'r')
while True:
    l = f.readline()
    if not l:
        break
    url_list = re.findall(r'<a href="([^\"]+)">([^<]+)</a>', l)
    print(url_list)
f.close()