
SQLITE_FILENAME = './DB_fds_offgridbox.sqlite'

TABLE_MCU = 'mcu'
TABLE_CHARGECONTROLLER = 'charge_controller'
TABLE_RELAYBOX = 'relay_box'
TABLE_RELAYSTATE = 'relay_state'


 # Define the State list
CC_STATE = ['Start', 'Night Check', 'Disconnected', 'Night', 'Fault!', 'MPPT', 'Absorption', 'FloatCharge', 'Equalizing', 'Slave']


remote_sql_create_charge_controller_table = """ CREATE TABLE IF NOT EXISTS charge_controller (
                                        id           integer PRIMARY KEY,
                                        boardId      text    NOT NULL,
                                        syncTime     date    NOT NULL,
                                        timestamp    date    NOT NULL,
                                        battsV       float   NOT NULL,
                                        battsSensedV float   NOT NULL,
                                        battsI       float   NOT NULL,
                                        arrayV       float   NOT NULL,
                                        arrayI       float   NOT NULL,
                                        statenum     integer NOT NULL,
                                        hsTemp       float   NOT NULL,
                                        rtsTemp      float   NOT NULL,
                                        outPower     float   NOT NULL,
                                        inPower      float   NOT NULL,
                                        minVb_daily  float   NOT NULL,
                                        maxVb_daily  float   NOT NULL,
                                        minTb_daily  float   NOT NULL,
                                        maxTb_daily  float   NOT NULL,
                                        dipswitches  text    NOT NULL
                                    ); """

remote_sql_create_relaybox_table = """ CREATE TABLE IF NOT EXISTS relay_box (
                                        id            integer PRIMARY KEY,
                                        boardId      text    NOT NULL,
                                        syncTime     date    NOT NULL,
                                        timestamp     date    NOT NULL,
                                        adc_vb        float   NOT NULL,
                                        adc_vch_1     float   NOT NULL,
                                        adc_vch_2     float   NOT NULL,
                                        adc_vch_3     float   NOT NULL,
                                        adc_vch_4     float   NOT NULL,
                                        t_mod         float   NOT NULL,
                                        global_faults integer NOT NULL,
                                        global_alarms integer NOT NULL,
                                        hourmeter_HI  float   NOT NULL,
                                        hourmeter_LO  float   NOT NULL,
                                        ch_faults_1   integer NOT NULL,
                                        ch_faults_2   integer NOT NULL,
                                        ch_faults_3   integer NOT NULL,
                                        ch_faults_4   integer NOT NULL,
                                        ch_alarms_1   integer NOT NULL,
                                        ch_alarms_2   integer NOT NULL,
                                        ch_alarms_3   integer NOT NULL,
                                        ch_alarms_4   integer NOT NULL
                                    ); """


remote_sql_create_relay_state_table = """ CREATE TABLE IF NOT EXISTS relay_state (
                                        id integer PRIMARY KEY,
                                        boardId      text    NOT NULL,
                                        syncTime     date    NOT NULL,
                                        timestamp     date    NOT NULL,
                                        relay_1   integer     NOT NULL,
                                        relay_2   integer     NOT NULL,
                                        relay_3   integer     NOT NULL
                                    ); """




remote_sql_create_mcu_table = """ CREATE TABLE IF NOT EXISTS mcu (
                                        id          integer     PRIMARY KEY,
                                        boardId      text    NOT NULL,
                                        syncTime     date    NOT NULL,
                                        timestamp   date        NOT NULL,
                                        temp1       float       NOT NULL,
                                        temp2       float       NOT NULL,
                                        pres1       float       NOT NULL,
                                        pres2       float       NOT NULL,
                                        pres3       float       NOT NULL,
                                        flux1       integer     NOT NULL,
                                        flux2       integer     NOT NULL,
                                        cc          float       NOT NULL,
                                        ac1         float       NOT NULL,
                                        ac2         float       NOT NULL
                                    ); """


def addDataTableMCU(boardId, data):
    query_data = list()
    for d in data:
        query_data.append( tuple([boardId,
                                      d['temp1'],
                                      d['temp2'],

                                      d['pres1'],
                                      d['pres2'],
                                      d['pres3'],
                                      d['flux1'],
                                      d['flux2'],

                                      d['cc'],
                                      d['ac1'],
                                      d['ac2'],
                                      d['timestamp']
                                      ]))

    query = "INSERT INTO " + TABLE_MCU + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?, ?, ?, ?,  ?, ?, ?, ?)"

    return query, query_data


def addDataTableChargeController(boardId, data):
    query_data = list()

    for d in data:
        query_data.append( tuple([boardId,
                                      d['timestamp'],
                                      d['battsV'],

                                      d['battsSensedV'],
                                      d['battsI'],
                                      d['arrayV'],
                                      d['arrayI'],
                                      d['statenum'],

                                      d['hsTemp'],
                                      d['rtsTemp'],
                                      d['outPower'],
                                      d['inPower'],
                                      d['minVb_daily'],

                                      d['maxVb_daily'],
                                      d['minTb_daily'],
                                      d['maxTb_daily'],
                                      d['dipswitches']
                                      ]))
    query = "INSERT INTO " + TABLE_CHARGECONTROLLER + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?, ?, ?, ?,   ?, ?, ?, ?, ?,  ?, ?, ?, ?)"

    return query, query_data



def addDataTableRelayState(boardId, data):
    query_data = list()

    for d in data:
        query_data.append( tuple([boardId,
                                      d['timestamp'],
                                      d['relay_1'],

                                      d['relay_2'],
                                      d['relay_3']
                                      ]))
    query = "INSERT INTO " + TABLE_RELAYSTATE + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?)"

    return query, query_data


def addDataTableRelayBox(boardId, data):
    query_data = list()

    for d in data:
        query_data.append( tuple([boardId,
                                      d['timestamp'],
                                      d['adc_vb'],

                                      d['adc_vch_1'],
                                      d['adc_vch_2'],
                                      d['adc_vch_3'],
                                      d['adc_vch_4'],
                                      d['t_mod'],

                                      d['global_faults'],
                                      d['global_alarms'],
                                      d['hourmeter_HI'],
                                      d['hourmeter_LO'],

                                      d['ch_faults_1'],
                                      d['ch_faults_2'],
                                      d['ch_faults_3'],
                                      d['ch_faults_4'],

                                      d['ch_alarms_1'],
                                      d['ch_alarms_2'],
                                      d['ch_alarms_3'],
                                      d['ch_alarms_4']
                                      ]))
    query = "INSERT INTO " + TABLE_RELAYBOX + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?, ?, ?, ?,    ?, ?, ?, ?,   ?, ?, ?, ?,   ?, ? ,?, ?)"

    return query, query_data
