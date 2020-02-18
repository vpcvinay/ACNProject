#### Python Version  

        --- Python v3.5.2

#### TEAM:

	--- Purna Chandra Vinay Kumar. Vemali
		https://github.com/vpcvinay/
		pxv171630@utdallas.edu

	--- Bennaghatta Narayanaswamy Pooja.
		https://github.com/PoojaGowda1617/
		pxb180017@utdallas.edu
		

### IMPLEMENTATION:

The project aims at implementing the funtionality of the Fog node, IoT node and the Cloud node in
distributed systems in the context of 
Fog computing. The program simulates a network of fog nodes in distributed systems, the cloud node
and the IoT nodes. By following the
instructions below on different server nodes, creates a network of fog nodes interlinked to each
other depending on the network we choose and all the fog nodes are connected to the cloud node. The
functionality of each part is described below.

#### IoT node (iot.py):

IoT node sends UDP requests to randomly choosen Fog nodes and receives responses from either the fog
node or the cloud node. The IoT node sends requests to the correspondind fog node's UDP port and
receives messages over a dedicated UDP port. Two child processes or threads are implemented, each to
send and receive requests to and from fog and cloud nodes. 

The IoT node process contains three functions 'Iot_node(obj)', 'Recv_comm(obj)' and 'Send_comm(obj)'
and takes an object of a class containing attributes as an argument. 

'Iot_node' function creates child processes over the target funtions 'Recv_comm', 'Send_comm' for
sending and receiving the messages. Once the count of the sent or received messages reaches the limit
of the number of requests, the threads terminates. The program prints the address of the Fog node
that the request sent to, the response to the request along with the IP addresses of the nodes that
the request hopped through.


#### Fog node (server.py):

When the fog node process starts, it listens over a listening port for incoming connections for
certain amount of time and if not all the neighbouring fog nodes are connected, then the node sends
connection request to the neighbouring fog nodes that it is not connected to including the cloud
node. 'conn_established' performs the above described action and once all the nodes are connected 
then the function creates 5 threads, 2 for IoT send and receive messages, 2 for Fog send and receive
message and 1 to send messages to cloud. 


#### Cloud node (cloud.py):

The functionality of cloud node is simple that it receives requests messages from fog nodes,
processes it and sends response directly to the IoT nodes. Only one cloud node is implemented. 

The main process creates 3 additional child processes, one to accept incoming connections from the 
fog nodes, one to receive messages from the fog and another to send messages to the IoT node.


### INSTRUCTIONS:

The inbuilt python3 compiler is used to run the python scripts. The instructions to run the scripts is as follows:

-> run the below commands:
for running the iot nodes
```
	$ python3 iot.py interval MY_UDP IP1 UDP1 IP2 UDP2 
	$ python3 iot.py 3 5000 "10.179.69.34" 6000 "10.179.69.35" 6001
```
for running the cloud node
```
	$ python3 cloud.py MY_TCP
	$ python3 cloud.py 8000
```

for running the FOG node
```
	$ python3 server.py Max_Response_Time t MY_TCP MY_UDP C TCP0 N1 TCP1 N2 TCP2 
	$ python3 server.py 9 3 7000 6000 "10.179.69.34" 8000 "10.179.69.35" 7001 "10.179.69.36" 7002
```

-->  Run the cloud node first and then bring up all the FOG nodes.  
-->  Wait for about 8-10 sec for all the nodes to connect.  
-->  Run the IoT node as many as required.  

For more details about the inputs refer to the document 'Implementation of FOG computing.pdf'
