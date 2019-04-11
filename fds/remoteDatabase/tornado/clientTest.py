import requests
import json

# SERVER_IP = 'localhost'
SERVER_IP = '25.46.34.214'

data_json = {"boardId" : "BOARD_001",
             "type" : 'cc',
             "data" : [{"minVb_daily": 22.547026137507025, "outPower": 24.275258060237544, "timestamp":"2019-04-08 13:48:00", "maxTb_daily": 0.6828438359255995, "minTb_daily": 12.397263250741739, "dipswitches":"00000001", "arrayV": 17.023912175049936, "battsI": 26.904394922364844, "battsV": 48.936773262478845, "rtsTemp": 14.623870818782692, "battsSensedV": 33.673276345273216, "inPower": 35.83499841283017, "synced": 0, "statenum": 1, "maxVb_daily": 28.57542407338068, "arrayI": 16.47622197315991, "id": 1, "hsTemp": 3.0901745780681877}, {"minVb_daily": 50.84640454791593, "outPower": 44.04890563658394, "timestamp":"2019-04-08 13:48:02", "maxTb_daily": 20.049260280790683, "minTb_daily": 23.577828516315495, "dipswitches":"00000001", "arrayV": 54.09429274884447, "battsI": 19.1006301009279, "battsV": 25.719117732200747, "rtsTemp": 56.18923402889119, "battsSensedV": 28.59332856068846, "inPower": 45.45498529868945, "synced": 0, "statenum": 8, "maxVb_daily": 37.44915723742729, "arrayI": 8.305311691682729, "id": 2, "hsTemp": 58.91314355572901}, {"minVb_daily": 13.499782396161503, "outPower": 22.13867764840377, "timestamp":"2019-04-08 13:48:04", "maxTb_daily": 17.214180893444126, "minTb_daily": 30.92484685576509, "dipswitches":"00000001", "arrayV": 50.24245958578742, "battsI": 28.893056053669095, "battsV": 10.613291094065648, "rtsTemp": 59.37534907518708, "battsSensedV": 37.64828499482793, "inPower": 9.006652901777809, "synced": 0, "statenum": 3, "maxVb_daily": 12.465538682371196, "arrayI": 7.166969970242009, "id": 3, "hsTemp": 32.042406003266876}]}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
payload = data=json.dumps(data_json)

r = requests.post("http://"+ SERVER_IP +":8888/cc", data=payload, headers=headers)
print("Response cc: ", r)
r = requests.post("http://"+ SERVER_IP +":8888/rb", data=payload, headers=headers)
print("Response rb: ", r)
r = requests.post("http://"+ SERVER_IP +":8888/rs", data=payload, headers=headers)
print("Response rs: ", r)
r = requests.post("http://"+ SERVER_IP +":8888/mcu", data=payload, headers=headers)
print("Response mcu: ", r)
