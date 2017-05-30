import os
fo=open('pb.7z','rb')
fw=open('pb1.7z','wb')
fo.seek(530032640)
filesize=os.stat('pb.7z').st_size
filesize-=530032640
recv_size=0
while not recv_size==filesize:
	if filesize - recv_size > 1024 * 4:
		data=fo.read(1024*4)
		recv_size+=len(data)
	else:
		data=fo.read(filesize - recv_size)
		recv_size=filesize
	fw.write(data)
fo.close()
fw.close()