import json


def openFile(fileName):
    try:
        f = open(fileName)
        return f
    except FileNotFoundError:
        print("file not found")
    except Exception as e:
        print(e)


f = openFile('C:/tmp/json.txt')
jt = []
for line in f:
    if line:
        jt.append(line)
f.close()
try:
    j = json.loads(''.join(jt))
except Exception as e:
    print(e)
