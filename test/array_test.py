# arr = ['aaa/1.html','aaab/8.html','aaa/2.html','aaa/3.html','aaab/8.html']
#
# arr2 = []
#
# for i in arr:
#     if i in arr2:
#         continue
#     else:
#         arr2.append(i)
#
# print(arr2)

# arr = 'a b c'.split(' ')
# print(len(arr))
# (a, b, c) = arr
# print(a)
# (c, d) = arr[:2]
# print(c)


import re
# pattern = re.compile('-?1?((?<=1)[01]|(?<!1)\d)')
pattern = re.compile('-?((\d)|(10)|(11))')
while True:
    i = input('str: ')
    if i == 'q':
        break
    if pattern.fullmatch(i):
        print('T')