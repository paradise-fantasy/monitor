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
