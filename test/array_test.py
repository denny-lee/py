arr = ['aaa/1.html','aaab/8.html','aaa/2.html','aaa/3.html','aaab/8.html']

arr2 = []

for i in arr:
    if i in arr2:
        continue
    else:
        arr2.append(i)

print(arr2)