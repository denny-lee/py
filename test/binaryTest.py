import binascii
str1 = b'e525737|Hattielhz)(05||e588063|*Twhzhz1155'
str2 = []
str3 = '404212200212220204220496288388464464420404432416488164160192212496496404212224224192216204496168336476416488416488196196212212'

def dec(str):
    cur = 0
    while cur < len(str):
        ch = str[cur:cur + 3]
        cur += 3
        str2.append(chr(int(ch)>>2))
    print(''.join(str2))


def enc(bb):
    for i in str1:
        print(i)

dec(str3)
# enc(str1)