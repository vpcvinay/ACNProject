
Python Version 
	--- Python v3.5.2

TEAM:
	--- Purna Chandra Vinay Kumar. Vemali
		https://github.com/vpcvinay/
		pxv171630
		2021380228

	--- Bennaghatta Narayanaswamy Pooja.
		https://github.com/PoojaGowda1617/
		pxb180017
		2021439541
	

INSTRUCTIONS:

The inbuilt python3 compiler is used to run the python scripts. The instructions to run the scripts is as follows:

-> run the below commands:
for running the iot nodes
	$ python3 iot.py interval MY_UDP IP1 UDP1 IP2 UDP2 
	$ python3 iot.py 3 5000 "10.179.69.34" 6000 "10.179.69.35" 6001

for running the cloud node
	$ python3 cloud.py MY_TCP
	$ python3 cloud.py 8000

for running the FOG node
	$ python3 server.py Max_Response_Time t MY_TCP MY_UDP C TCP0 N1 TCP1 N2 TCP2 
	$ python3 server.py 9 3 7000 6000 "10.179.69.34" 8000 "10.179.69.35" 7001 "10.179.69.36" 7002

-> Run the cloud node first and then bring up all the FOG nodes. 
-> Wait for about 8-10 sec for all the nodes to connect.
-> Run the IoT node as many as required.
