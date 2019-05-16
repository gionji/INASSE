# INASSE

## Install on NEO Ubuntu 14.04
```
sudo apt-get update
sudo apt-get upgrade
git clone https://github.com/gionji/INASSE
cd INASSE/fds/gateway/core/src03/
sudo pip install --upgrade pip
sudo apt-get install python-eventlet
sudo apt-get install python-pymodbus
sudo pip install --upgrade setuptools
sudo pip install smbus2
```

### test
```
sudo python test.py -s 192.168.1.181 --modbus-debug --mcu-debug
```
### Tanzania test
```
sudo python3 test.py -i 1 -server-addr <FULL_REMOTE_SERVER_PATH>
```
