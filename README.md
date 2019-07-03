# INASSE

## Install on NEO Ubuntu 14.04


### update the system
```
sudo apt-get update
sudo apt-get upgrade
```

### get The code
```
git clone https://github.com/gionji/INASSE
cd INASSE/fds/gateway/core/src03/
```

### Python 2 ( UDoo Neo )
```
sudo pip install --upgrade pip
sudo apt-get install python-eventlet
sudo apt-get install python-pymodbus
sudo pip install --upgrade setuptools
sudo pip install smbus2
```

### Pyhton 3 
```
sudo apt install python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade setuptools
sudo pip3 install requests
sudo pip3 install eventlet
sudo pip3 install pymodbus
sudo pip3 install smbus2
```

### test
```
sudo python3 test.py -i 3 --modbus-debug -p m

sudo python test.py -s 192.168.1.181 --modbus-debug --mcu-debug
```
### Tanzania test
```
sudo python3 test.py -i 1 -server-addr <FULL_REMOTE_SERVER_PATH>
```
