from socket import *
import socket
import sys
import threading
import pickle
import re
import os
import time
import datetime
from struct import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servip = ('152.46.19.77')
#serverip = (socket.gethostbyname(socket.gethostname())
timedict = {}
timedict[1]=[]
timedict[2]=[]
timedict[3]=[]
timedict[4]=[]
timedict[5]=[]
if os.path.exists('time.pkl'):
	with open('time.pkl', 'rb') as f1:
		timedict=pickle.load(f1)
print (servip)
#server_address = [(servip, 7735)]
server_address = []
serv_port = int(sys.argv[len(sys.argv)-3])
file_name = sys.argv[len(sys.argv)-2]
MSS = int(sys.argv[len(sys.argv)-1])
argindex = 1
while argindex < len(sys.argv)-3:
	appendval=(sys.argv[argindex],serv_port)
	server_address.append(appendval)
	argindex+=1

print(socket.gethostbyname(socket.gethostname()))
client_address = (socket.gethostbyname(socket.gethostname()),8976)
print (client_address)
sock.bind(client_address)
ack=[0,0,0,0,0]
path = 'client/'
if not os.path.exists(path):
		os.makedirs(path);

'''

for name in os.listdir(path):
	print (name)
	sock.sendto(name.encode('utf-8'), server_address);
	with open(os.path.join(path, name), 'rb') as f:
		while True:
			data=f.read(1024)
			sock.sendto(data, server_address);
			print (len(data))
			if len(data)<1024:
				print ("done")
				break
			time.sleep(0.1)
#sock.sendto(message1.encode('utf-8'), server_address)
#sock.sendto(message2.encode('utf-8'), server_address)'''

def ackrecv():
	global ack
	global seq
	while True:
		success=1
		ackpacket, address = sock.recvfrom(1024)
		#print ("ackpacket is: ",ackpacket)
		ackseq=unpack('>L', ackpacket[0:4])[0]
		if ackseq==seq:
			ack[server_address.index(address)]=1
		#print (ack)
		
def timefun(data,seq):
	timer = threading.Timer(0.5, resend, args=(data,seq))
	timer.start()
	#print ("seq is:", seq)
	while True:
		if 0 not in ack[0:len(server_address)]:
			timer.cancel()
			#print ("seq no, timer closed", seq)
			break
	
def resend(data,seq):
	print ("Timeout, sequence number = ", seq)
	print ("Resending packet with seq number:", seq)
	packsend(data)
	timefun(data,seq)


def encap(packet,seq):
	seq=pack('>L',seq)
	ind=pack('>H',21845)
	#print (packet)
	check=checksum(packet)
	check=pack('>H',check)
	#print (check)
	header=seq+check+ind
	#print (header)
	#print (len(header))
	modpacket=header+packet
	return (modpacket)
	
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
	
def packsend(packet):
	global server_address
	global ack
	for server in server_address:
		if ack[server_address.index(server)]==0:
			sock.sendto(packet, server);

		
def sendfun(file_name, MSS):
	one=1
	global seq
	global path
	global ack
	global server_address
	global timedict
	seq=0
	packsend(encap(file_name.encode('utf-8'),seq))
	print ("sent")
	seq+=1
	t1 = time.time()
	with open(os.path.join(path, file_name), 'rb') as f:
		while True:
			
			data=f.read(MSS)
			data = encap(data,seq)
			#print (data)
			ack=[0,0,0,0,0]
			packsend(data)
			#print ("sending data with seq:", seq)
			timethread=threading.Thread(target=timefun, args=(data,seq))
			timethread.daemon=True
			timethread.start()
			while True:
				success=1
				for server in server_address:
					if ack[server_address.index(server)]==0:
						success=0
				if success==1:
					break
			seq = seq+1
			time.sleep(0.05)
			
			if len(data)<MSS:
				print ("file sent")
				t2 = time.time()
				break
			
	diff = t2 - t1
	timedict[len(server_address)].append(diff)
	pickle.dump(timedict, open('time.pkl', 'wb'))
	print (timedict)
	"""	timethread=threading.Thread(target=timefun)
		timethread.daemon = True
		timethread.start()
		while True:
				
	"""
	
	
def main():
	#file_name = input("Please enter the name of the file to be transferred: ")
	#MSS = input("\nPlease enter the Maximmum segment size (MSS) for transferring data: ")
	#MSS=int(MSS)
	global seq
	global file_name
	#global MSS
	ackthread = threading.Thread(target=ackrecv)
	ackthread.daemon = True
	ackthread.start()
	
	sendthread = threading.Thread(target=sendfun, args=(file_name,MSS))
	sendthread.daemon = True
	sendthread.start()
	
	while True:
		qwe=1
		
if __name__ == '__main__':
    main();




