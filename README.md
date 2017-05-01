# monitor
Program to monitor paradise computers, pies and other devices

## Installation (Manager)
Install `snmp`, `snmpd`, and `snmp-mibs-downloader`  with:
``` 
sudo apt-get install snmp snmpd snmp-mibs-downloader
```

Install pip-dependencies with:
```
pip install -r requirements.txt
```

Edit the file `/etc/snmp/snmp.conf`, comment out everything.

Place the `ca.crt`-file into the project folder.

## Adding more hosts
Monitored hosts do not need to clone this repo, only the manager host is required to use this. In order to add a monitored host, install `snmpd` on the host.

Open `/etc/snmp/snmpd.conf`, remove everything and add:
```
view systemonly included .1.3.6.1.2.1.1
view systemonly included .1.2.6.1.2.1.25.1

rocommunity  paradise 129.241.208.0/23
rocommunity  paradise 127.0.0.1

syslocation paradise
syscontact paradise
```

Then restart `snmpd`:
```
sudo service snmpd restart
```

On the manager host, add a line to the `hosts.txt` in the project folder:
```
[monitored host IP];[community];[display-name (arbitrary)]
```
E.g.
```
129.241.209.54;paradise;tormodVMWare
```

## Run as cron-job
Run `crontab -e`
Create your cron-job, e.g. 
```
5,10,15,20,25,30,35,40,45,50,55 * * * * python /monitor-folder/main.py
``` 
