# RideSharing
Ride Sharing App in Python

==========================
		User Manual
==========================

Server : ridesharing_app.py
Client : passenger.py, driver.py

-------------
passenger.py
-------------
After you got connected, send your presence using this command below
command : PRESENCE <your name>
eg : PRESENCE alice

After you got reply message from server, you can make a request using this command below
command : REQUEST

After a driver accepted your request, you will get the location of the driver, just wait

----------
driver.py
----------
After you got connected, send your presence using this command below
command : PRESENCE <your name>
eg : PRESENCE bob

Just wait until a request pop up.
To accept a request from a passenger, use this command below
command : ACCEPT <passenger's name>
eg: ACCEPT alice

You can start the trip using this command below
command : START
The server will receive driver's name and passenger's name

You can end the trip using this command below
command : END
The server will receive driver's name, passenger's name, distance in kilometer, and the duration of the trip