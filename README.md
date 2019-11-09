# p2mp-ftp
Point-to-Multipoint File Transfer Protocol

This project was done as part of the coursework under CSC 573 Internet Protocols at NC State University. 

The main functionality of the project is provide a reliable file transfer service using UDP by implementing a Stop-and-Wait ARQ at the application level. A single sender can then send the same file to multiple receivers at the same time with accountablity for packet losses. 

1.	The server code can be found in the script file named p2mpserver.py done using Python3.
2.	The client code can be found in the script file named p2mpclient.py done using Python3. 
3.	The server code is run followed by the client code to enable point to multipoint data transfer.
4.	Please make sure the file to be sent is available in a folder named client which is to be created in the same directory from which the client code is being run.
5.	While running the client code through command line, the arguments can be passed in command line in the following order � server1IP server2IP server3IP serverportno file-name MSS (this is the case of 3 servers).
6.	While running the server code through command line, the arguments can be passed in command line in the following order � serverportno file-name probability-factor. Here the file-name is the file to which the received data will be written into.
7.	The file after downloading can be seen in a folder named server in the same directory from which the server code is run.


