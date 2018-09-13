#!/usr/bin/env python
# _*_ coding: utf-8

import sys
import re
import http.client as client

ROOT = '$root$'
if len(sys.argv) != 2:
    exit()
ROOT_URL = (ROOT, sys.argv[1])

visited = [sys.argv[1]]

DIR = 'C:/manual/spring_frame'


def parseUrl(url):
    ssl = False
    if '://' in url:
        ssl = url.split('://')[0] == 'https'
        url = url.split('://')[1]

    if '/' not in url:
        targetPage = '/'
        domain = url
    else:
        idx = url.index('/')
        (domain, targetPage) = (url[:idx], url[idx:])
    return domain, targetPage, ssl


def reader(url):
    (base, target, ssl) = parseUrl(url)
    if ssl:
        conn = client.HTTPSConnection("10.248.192.245:80")
    else:
        conn = client.HTTPConnection("10.248.192.245:80")

    conn.set_tunnel(base)
    conn.request("GET", target)
    data = conn.getresponse()
    stat = data.status
    print('status is ----------- %d' % stat)
    if stat <= 200:
        content = data.read().decode('utf-8')
    else:
        content = None

    conn.close()
    return content


def parse(content):
    if content:
        url_list = re.findall(r'<a href="([^\"]+)">([^<]+)</a>', content)
        return url_list

    return None


def keepItem(it):
    global visited
    if it in visited:
        return False
    else:
        visited.append(it)
        return True


def write_content(name, content):
    if name == ROOT:
        file = open(DIR + '/index.html', 'w')
    else:
        file = open(DIR + '/' + name.replace(' ', '_') + '.html', 'w')
    file.write(content)
    file.close()


def digDoc(pair, depth):

    (name, url) = pair
    content = reader(url)
    write_content(name, content)

    if depth > 1:
        return

    ulist = parse(content)
    if ulist:
        for (href, label) in ulist:
            # print('  ' * depth + label + ' - ' + href)
            if href.startswith('/') or href.startswith('http'):
                continue
            elif '#' in href:
                nhref = sys.argv[1] + href.split('#')[0]
            else:
                nhref = sys.argv[1] + href

            if not keepItem(nhref):
                continue
            # print('  ' * depth + label + ' - ' + nhref)
            digDoc((label, nhref), depth + 1)


digDoc(ROOT_URL, 1)
