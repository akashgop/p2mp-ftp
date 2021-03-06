# p2mp-ftp
Point-to-Multipoint File Transfer Protocol

This project was done as part of the coursework under CSC 573 Internet Protocols at NC State University. 

The main functionality of the project is provide a reliable file transfer service using UDP by implementing a Stop-and-Wait ARQ at the application level. A single sender can then send the same file to multiple receivers at the same time with accountablity for packet losses. 

1.	The server code can be found in the script file named p2mpserver.py done using Python3.
2.	The client code can be found in the script file named p2mpclient.py done using Python3. 
3.	The server code is run followed by the client code to enable point to multipoint data transfer.
4.	Please make sure the file to be sent is available in a folder named client which is to be created in the same directory from which the client code is being run.
5.	While running the client code through command line, the arguments can be passed in command line in the following order : 'server1 IPaddress' 'server2 IPaddress' 'server3 IPaddress' 'server port no' 'file name' 'Maximum Segment Size' (this is the case of 3 servers).
6.	While running the server code through command line, the arguments can be passed in command line in the following order : 'server port no' 'file-name' 'probability-factor'. Here the file-name is the file to which the received data will be written into.
7.	The file after downloading can be seen in a folder named server in the same directory from which the server code is run.
8. The Maximum segment size variable is to set the maxmimum segment size transferred at a time in bytes and can be between 100 and 1000 ideally. The probability factor is the probability that the server drops a received segment and can be in the range of 0.01 to 0.1.
9. The server port number to be followed here is assigned to a UDP socket at the server and has to be a well known port for the client.

