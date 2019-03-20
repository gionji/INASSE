
CHARGE_CONTROLLER_UNIT = 0x01
RELAYBOX_UNIT          = 0x09
MODBUS_PORT            = 502
CHARGE_CONTROLLER_IP   = '192.168.0.253'

SQLITE_FILENAME = './DB_fds_offgridbox.sqlite'


'''


MCU_DEBUG_CMD = 'd'
MCU_READ_CMD = 'r'
MCU_LIST_PARAM_CMD = 'l'
MCU_PING_CMD = 'p'




AWS_URL  = "fabbrica-del-sole.c91brofc69ac.us-east-2.rds.amazonaws.com"
AWS_USER = "fds_master"
AWS_PASS = "123qweASD"
AWS_DB   = "offgridbox"
'''


 # Define the State list
CC_STATE = ['Start', 'Night Check', 'Disconnected', 'Night', 'Fault!', 'MPPT', 'Absorption', 'FloatCharge', 'Equalizing', 'Slave']


sql_create_charge_controller_table = """ CREATE TABLE IF NOT EXISTS charge_controller (
                                        id           integer PRIMARY KEY,
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
                                        dipswitches  text    NOT NULL,
                                        synced       integer(1) default 0
                                    ); """

sql_create_relaybox_table = """ CREATE TABLE IF NOT EXISTS relay_box (
                                        id            integer PRIMARY KEY,
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
                                        ch_alarms_4   integer NOT NULL,
                                        synced        integer(1) default 0
                                    ); """


sql_create_mcu_table = """ CREATE TABLE IF NOT EXISTS mcu (
                                        id integer PRIMARY KEY,
                                        timestamp         date      NOT NULL,
                                        brick_baro_pres   float     NOT NULL,
                                        brick_temp        float     NOT NULL,
                                        brick_baro_temp   float     NOT NULL,
                                        brick_light       float     NOT NULL,
                                        brick_hum         float     NOT NULL,
                                        a0                integer   NOT NULL,
                                        a1                integer   NOT NULL,
                                        a2                integer   NOT NULL,
                                        a3                integer   NOT NULL,
                                        a4                integer   NOT NULL,
                                        a5                integer   NOT NULL,
                                        synced            integer(1) default 0
                                    ); """


sql_create_relay_state_table = """ CREATE TABLE IF NOT EXISTS relay_state (
                                        id integer PRIMARY KEY,
                                        timestamp     date    NOT NULL,
                                        relay_1   integer     NOT NULL,
                                        relay_2   integer     NOT NULL,
                                        relay_3   integer     NOT NULL,
                                        synced    integer(1)  default 0
                                    ); """

# ADD DATA TO SQLITE DB QUERIES
insert_relay_state = """ 
                     INSERT INTO relay_state (id, relay_1, relay_2, relay_3, timestamp)
                     VALUES (NULL, :relay_1, :relay_2, :relay_3, datetime('now'));
                     """

insert_mcu = """ 
             INSERT INTO mcu (id, brick_light, brick_temp, brick_baro_temp, brick_baro_pres, brick_hum, 
             a0, a1, a2, a3, a4, a5, timestamp)
             VALUES
             (NULL, :brick_light, :brick_temp, :brick_baro_temp, :brick_baro_pres, :brick_hum, 
             :a0, :a1, :a2, :a3, :a4, :a5, datetime('now'));
             """

insert_rb = """ 
            INSERT INTO relay_box (id, ch_alarms_3, hourmeter_LO, 
              ch_faults_1, ch_alarms_1, 
              ch_faults_3, ch_faults_2, ch_alarms_4, ch_faults_4, hourmeter_HI, 
              adc_vb, adc_vch_4, adc_vch_1, adc_vch_2, adc_vch_3, 
              t_mod, global_faults, global_alarms, ch_alarms_2 , timestamp)
            VALUES (NULL, :ch_alarms_3, :hourmeter_LO, :ch_faults_1, :ch_alarms_1,
              :ch_faults_3, :ch_faults_2, :ch_alarms_4, :ch_faults_4, :hourmeter_HI, 
              :adc_vb, :adc_vch_4, :adc_vch_1, :adc_vch_2, :adc_vch_3, 
              :t_mod, :global_faults, :global_alarms, :ch_alarms_2, datetime('now') );
            """

insert_cc = """ 
            INSERT INTO charge_controller (id, outPower, minTb_daily, dipswitches, 
                                               arrayV, minVb_daily, arrayI, battsSensedV, 
                                               statenum, maxTb_daily, battsI, battsV, rtsTemp, 
                                               inPower, maxVb_daily, hsTemp, timestamp )
            VALUES                 
                  (NULL, :outPower, :minTb_daily, :dipswitches, 
                  :arrayV, :minVb_daily, :arrayI, :battsSensedV,
                  :statenum, :maxTb_daily, :battsI, :battsV, :rtsTemp,
                  :inPower, :maxVb_daily, :hsTemp, datetime('now')  );
            """


# ADD DATA TO MYSQL DB QUERIES
insert_relay_state_mysql = """ 
                     INSERT INTO relay_state (id, relay_1, relay_2, relay_3, timestamp)
                     VALUES (NULL, :relay_1, :relay_2, :relay_3, datetime('now'));
                     """

insert_mcu_mysql = """ 
             INSERT INTO mcu (id, brick_light, brick_temp, brick_baro_temp, brick_baro_pres, brick_hum, 
             a0, a1, a2, a3, a4, a5, timestamp)
             VALUES
             (NULL, :brick_light, :brick_temp, :brick_baro_temp, :brick_baro_pres, :brick_hum, 
             :a0, :a1, :a2, :a3, :a4, :a5, datetime('now'));
             """

insert_rb_mysql = """ 
            INSERT INTO relay_box (id, ch_alarms_3, hourmeter_LO, 
              ch_faults_1, ch_alarms_1, 
              ch_faults_3, ch_faults_2, ch_alarms_4, ch_faults_4, hourmeter_HI, 
              adc_vb, adc_vch_4, adc_vch_1, adc_vch_2, adc_vch_3, 
              t_mod, global_faults, global_alarms, ch_alarms_2 , timestamp)
            VALUES (NULL, :ch_alarms_3, :hourmeter_LO, :ch_faults_1, :ch_alarms_1,
              :ch_faults_3, :ch_faults_2, :ch_alarms_4, :ch_faults_4, :hourmeter_HI, 
              :adc_vb, :adc_vch_4, :adc_vch_1, :adc_vch_2, :adc_vch_3, 
              :t_mod, :global_faults, :global_alarms, :ch_alarms_2, datetime('now') );
            """

insert_cc_mysql = """ 
            INSERT INTO charge_controller (id, outPower, minTb_daily, dipswitches, 
                                               arrayV, minVb_daily, arrayI, battsSensedV, 
                                               statenum, maxTb_daily, battsI, battsV, rtsTemp, 
                                               inPower, maxVb_daily, hsTemp, timestamp )
            VALUES                 
                  (NULL, :outPower, :minTb_daily, :dipswitches, 
                  :arrayV, :minVb_daily, :arrayI, :battsSensedV,
                  :statenum, :maxTb_daily, :battsI, :battsV, :rtsTemp,
                  :inPower, :maxVb_daily, :hsTemp, datetime('now')  );
            """


# QUERIES
GET_CC_DATA_IDS  = '''SELECT id FROM charge_controller WHERE synced = 0 LIMIT 300; '''
GET_RB_DATA_IDS  = '''SELECT id FROM relay_box         WHERE synced = 0 LIMIT 300; '''
GET_RS_DATA_IDS  = '''SELECT id FROM relay_state       WHERE synced = 0 LIMIT 300; '''
GET_MCU_DATA_IDS = '''SELECT id FROM mcu               WHERE synced = 0 LIMIT 300; '''

GET_CC_DATA  = '''SELECT timestamp, battsV, battsSensedV, battsI, arrayV, arrayI, statenum, 
                         hsTemp, rtsTemp, outPower, inPower, minVb_daily, maxVb_daily, 
                         minTb_daily,  maxTb_daily, dipswitches 
                  FROM charge_controller 
                  WHERE id IN ('''


GET_RB_DATA  = '''SELECT timestamp, adc_vb, adc_vch_1, adc_vch_2, adc_vch_3, adc_vch_4, 
                         t_mod, global_faults, global_alarms, hourmeter_HI, hourmeter_LO,
                         ch_faults_1, ch_faults_2, ch_faults_3, ch_faults_4, 
                         ch_alarms_1, ch_alarms_2, ch_alarms_3, ch_alarms_4
                  FROM relay_box         
                  WHERE id IN ('''


GET_RS_DATA  = '''SELECT timestamp, relay_1, relay_2, relay_3
                  FROM relay_state         
                  WHERE id IN ('''


GET_MCU_DATA = '''SELECT timestamp, brick_baro_pres, brick_temp, brick_baro_temp, brick_light, brick_hum, 
                         a0, a1, a2, a3, a4, a5                  
                  FROM mcu       
                  WHERE id IN ('''
