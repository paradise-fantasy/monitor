# monitor
Program to monitor paradise computers, pies and other devices

## Installation
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



On the manager host and add a line to the `hosts.txt` in the project folder:
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
