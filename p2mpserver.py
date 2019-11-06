from socket import *
import socket
import sys
import threading
import pickle
import re
import os
import time
from struct import *
import random

servip = (socket.gethostbyname(socket.gethostname()))
print (servip)
try:
	lossprob = float(sys.argv[3])
	file_name = sys.argv[2]
	serv_port = int(sys.argv[1])
except:
	lossprob = 0.05
	file_name = 'random.pdf'
	serv_port = 7735
	
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (servip, serv_port)
MSS=1024
sock.bind(server_address)


def checksum(packet):
	i=0
	check=0
	while True:
		a=ord(packet[i:i+1])
		try:
			b=ord(packet[i+1:i+2])
		except:
			b=0
		check+=(256*a)+b
		check=(check//65536)+(check%65536)
		try:
			packet[i+1]
		except:
			break
		i+=1
	#print (check)
	return check

def acksend(orgdata,address,expseq):
	calccheck=checksum(decap(orgdata))
	#print (calccheck)
	recvdcheck=unpack('>H',orgdata[4:6])[0]
	#print (recvdcheck)
	#print (orgdata[4:6])
	recvdseq=unpack('>L',orgdata[0:4])[0]
	if recvdseq==expseq:
		if calccheck==recvdcheck:
			sock.sendto(ackgen(orgdata), address)
			return (1)
	elif calccheck==recvdcheck:
		sock.sendto(ackgen1(orgdata,expseq), address)
		return (0)


def ackgen1(orgdata, expseq):
	seq=expseq-1
	seq=pack('>L',seq)
	ind=pack('>H',43690)
	zer=pack('>H',0)
	ackpacket=seq+zer+ind
	return (ackpacket)
	
	
def ackgen(orgdata):
	seq=orgdata[0:4]
	ind=pack('>H',43690)
	zer=pack('>H',0)
	ackpacket=seq+zer+ind
	return (ackpacket)

def decap(data):
	data=data[8:len(data)]
	return (data)
	

def funs():
	#time.sleep(5)
	name, address = sock.recvfrom(1024)
	name=decap(name)
	#print (name)
	first=1
	expseq=1
	path = 'server/'
	if not os.path.exists(path):
		os.makedirs(path);
	while True:
		data, address = sock.recvfrom(1024)
		orgdata=data
		#print (orgdata)
		chance=random.random()
		if chance<lossprob:
			print("Packet Loss,sequence number = ", expseq)
		if chance>lossprob:
			okay=acksend(orgdata,address,expseq)
			if okay==1:
				expseq+=1
				data=decap(data)
				if first==1:
					print("Start Time: ",time.time())
					MSS=len(data)
					first+=1
					with open(os.path.join(path, file_name), 'wb') as f:
						f.write(data)
				else:	
					with open(os.path.join(path, file_name), 'ab') as f:
						f.write(data)
						#print (data)
				if len(data)<MSS:
					print("End Time: ", time.time())
					print ("file received")
					break
	#print (data.decode('utf-8'))
	#data, address = sock.recvfrom(1000)
	#print (data.decode('utf-8'))


def main():
	thread1 = threading.Thread(target=funs)
	thread1.daemon=True
	thread1.start()
	print ("Done")
	while 1:
		a=2
		
if __name__ == '__main__':
    main();
