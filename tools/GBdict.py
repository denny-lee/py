#!/usr/bin/env python
# _*_ coding: utf-8
import re
import http.client as client
import os
import pytz
from datetime import datetime
from datetime import timezone
from datetime import timedelta

controllerMappingFile = 'c:/Users/e657183/Desktop/ESP_dev_manual/esp_controller_map.txt'
lbFile = 'c:/Users/e657183/Desktop/ESP_dev_manual/loadbalance_host.txt'
viewMap = None
URL = 'url '
PBRUN = 'pb '
HELP = ('?', 'h')
Q = ('q', 'Q')
PW = 'pw'
CODE = 'code '
LB = 'lb'
ADD = ':a'
TM = 'tm '
outputCache = ''
help_doc = 'Usage:\n--------------------Search Cmd--------------------\n' \
           'pb {hostname}\n' \
           'url {/path} : to seach Controllers\n' \
           '{instance} [env]\n' \
           'pw\n' \
           'tm {timestamp} [from_tm_zone] [to_tm_zone]\n' \
           'code {instance} [env]\n' \
           'lb\n' \
           '? or h for HELP\n' \
           'q or Q for Quit\n' \
           '---------------------------------------------------\n\n'
pw_doc = ''
diamond = '404212200212220204220496288388464464420404432416488164160192212496496404212224224192216204496168336476416488416488196196212212'
code_version_url = 'http://esp-%s-code.statestr.com:5506/%s/code/artifactory_version.txt'
property_url = 'http://esp-%s-code.statestr.com:5506/%s/resources/helium.properties'
property_url_1 = 'http://gdcul1908.statestr.com:81/%s/resources/helium.properties'

pattern = re.compile('-?((\d)|(10)|(11))')


def _dec(s):
    cur = 0
    arr = []
    while cur < len(s):
        ch = s[cur:cur + 3]
        cur += 3
        arr.append(chr(int(ch)>>2))
    return ''.join(arr)


def PRT(str):
    global outputCache
    outputCache = str
    print(str)


def openFile(fileName):
    try:
        f = open(fileName)
        return f
    except FileNotFoundError:
        print("file not found")
    except Exception as e:
        print(e)

def showTxt(f):
    if not f:
        return
    for line in f:
        print(line[:-1])
    f.close()


def parseControllerMapping(f):
    if not f:
        return
    global viewMap
    try:
        list = []
        for line in f:
            if not line.startswith('/') or line.startswith('/\t'):
                continue
            m = re.search('^(.+?)\s+.*src/modules/.+?/(.*)', line)
            if m:
                list.append((m.group(1), m.group(2).replace('/', '.')))
        if list:
            viewMap = dict(list)
        else:
            print('no mapping found')
    except Exception as e:
        print(e)
    finally:
        f.close()


def fetchController(url):
    if not viewMap:
        return
    for k, v in viewMap.items():
        if re.search(url, k):
            print(k, '->', v)


def convertSpecial(inst, env):
    if inst == 'ent2':
        if env == 'cuat':
            return property_url % ('buat', 'imsmocuat')
        else:
            return property_url % (env, 'artisan')
    elif inst == 'ais':
        if env == 'qa':
            return property_url_1 % 'aisqa'
        elif env == 'buat':
            return property_url % (env, 'aismis')
    if env == 'cuat':
        if not inst.endswith('c'):
            return property_url % ('buat', inst + 'c')
    return property_url % (env, inst)


def readFromUrl(url):
    if not url:
        return
    conn = None
    try:
        m = re.search('http[s]?://([^:]+(:\d{2,5})?)([^:]+)', url)
        conn = client.HTTPConnection(m.group(1))
        conn.request('GET', m.group(3))
        data = conn.getresponse()
        if data and data.status == 200:
            print(data.read().decode())
    except Exception as e:
        print(e)
    finally:
        conn.close()


def getTime(t, tzf, tzt):
    if not t or not re.fullmatch('\d+', t):
        return
    if tzf and tzt:
        try:
            tz1 = getTimeZone(tzf)
            tz2 = getTimeZone(tzt)
            tmp = datetime.fromtimestamp(float(t) / 1000, tz=tz1)
            time = tmp.astimezone(tz2)
            print(time)
            return
        except pytz.UnknownTimeZoneError as e:
            print('Unknown TimeZone: %s' % e)

    time = datetime.fromtimestamp(float(t) / 1000)
    print(time)


def getTimeZone(tz):
    if not tz:
        return None
    if pattern.match(tz):
        if tz.startswith('-'):
            h = - int(tz[1:])
        else:
            h = int(tz)
        return timezone(timedelta(hours=h))
    else:
        return pytz.timezone(tz)

def execute(c):
    if not c:
        return
    c = c.strip()
    if c in HELP:
        print(help_doc)
    elif c.startswith(PBRUN):
        host = c[len(PBRUN):]
        PRT('pbrun -u monitor -h ' + host + ' firecloudvm')
    elif c == PW:
        pw = _dec(diamond).split('||')
        arr = []
        for i in pw:
            (u, p) = i.split('|')
            arr.append('user: ' + u + '\tpass: ' + p)
        PRT("\n".join(arr))
    elif c.startswith(URL):
        url = c[len(URL):]
        fetchController(url)
    elif c.startswith(CODE):
        (inst, env) = c.split(' ')[1:]
        url = code_version_url % (env, inst)
        PRT(url)
        readFromUrl(url)
    elif c == LB:
        showTxt(openFile(lbFile))
    elif c.startswith(TM):
        time = c[len(TM):]
        (tm_zone, to_tm_zone) = (None, None)
        if ' ' in time:
            time_arr = time.split(' ')
            if len(time_arr) == 3:
                (time, tm_zone, to_tm_zone) = time_arr
            else:
                print('timezone ignore, Usage: fromTmZone toTmZone')
        getTime(time, tm_zone, to_tm_zone)
    elif c == ADD:
        print('add things')
    elif c == 'cls':
        os.system(c)
    else:
        if ' ' in c:
            try:
                (inst, env) = c.split(' ')
                url = convertSpecial(inst, env)
                PRT(url)
                readFromUrl(url)
            except:
                print('Usage: {instance} {env}\n or ? for Help')
        else:
            print('I don\'t understand.')


def init():
    print(help_doc)
    parseControllerMapping(openFile(controllerMappingFile))


init()
while True:
    cmd = input(">> ")
    if cmd in Q:
        break
    else:
        # print('Command: '+cmd+'\n')
        execute(cmd)
print("Bye~")
