import FdsCommon as fds


SQLITE_FILENAME = 'DB_fds_offgridbox.sqlite'


 # Define the State list
CC_STATE = ['Start', 'Night Check', 'Disconnected', 'Night', 'Fault!', 'MPPT', 'Absorption', 'FloatCharge', 'Equalizing', 'Slave']


sql_create_charge_controller_table = """ CREATE TABLE IF NOT EXISTS charge_controller (
                                        id           integer PRIMARY KEY,
                                        timestamp    date    NOT NULL,
                                        """ + fds.LABEL_CC_BATTS_V + """     float   NOT NULL,
                                        """ + fds.LABEL_CC_BATT_SENSED_V + """ float   NOT NULL,
                                        """ + fds.LABEL_CC_BATTS_I + """        float   NOT NULL,
                                        """ + fds.LABEL_CC_ARRAY_V + """        float   NOT NULL,
                                        """ + fds.LABEL_CC_ARRAY_I + """        float   NOT NULL,
                                        """ + fds.LABEL_CC_STATENUM + """      integer NOT NULL,
                                        """ + fds.LABEL_CC_HS_TEMP + """        float   NOT NULL,
                                        """ + fds.LABEL_CC_RTS_TEMP + """       float   NOT NULL,
                                        """ + fds.LABEL_CC_OUT_POWER + """      float   NOT NULL,
                                        """ + fds.LABEL_CC_IN_POWER + """       float   NOT NULL,
                                        """ + fds.LABEL_CC_MINVB_DAILY + """   float   NOT NULL,
                                        """ + fds.LABEL_CC_MAXVB_DAILY + """   float   NOT NULL,
                                        """ + fds.LABEL_CC_MINTB_DAILY + """   float   NOT NULL,
                                        """ + fds.LABEL_CC_MAXTB_DAILY + """   float   NOT NULL,
                                        """ + fds.LABEL_CC_DIPSWITCHES + """   text    NOT NULL,
                                        synced       integer(1) default 0
                                    ); """



sql_create_relaybox_table = """ CREATE TABLE IF NOT EXISTS relay_box (
                                        id            integer PRIMARY KEY,
                                        timestamp     date    NOT NULL,
                                        """ + fds.LABEL_RB_VB + """         float   NOT NULL,
                                        """ + fds.LABEL_RB_ADC_VCH_1 + """      float   NOT NULL,
                                        """ + fds.LABEL_RB_ADC_VCH_2 + """      float   NOT NULL,
                                        """ + fds.LABEL_RB_ADC_VCH_3 + """      float   NOT NULL,
                                        """ + fds.LABEL_RB_ADC_VCH_4 + """      float   NOT NULL,
                                        """ + fds.LABEL_RB_T_MOD + """          float   NOT NULL,
                                        """ + fds.LABEL_RB_GLOBAL_FAULTS + """  integer NOT NULL,
                                        """ + fds.LABEL_RB_GLOBAL_ALARMS + """  integer NOT NULL,
                                        """ + fds.LABEL_RB_HOURMETER_HI + """   float   NOT NULL,
                                        """ + fds.LABEL_RB_HOURMETER_LO + """   float   NOT NULL,
                                        """ + fds.LABEL_RB_CH_FAULTS_1 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_FAULTS_2 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_FAULTS_3 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_FAULTS_4 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_ALARMS_1 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_ALARMS_2 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_ALARMS_3 + """    integer NOT NULL,
                                        """ + fds.LABEL_RB_CH_ALARMS_4 + """    integer NOT NULL,
                                        synced        integer(1) default 0
                                    ); """


sql_create_relay_state_table = """ CREATE TABLE IF NOT EXISTS relay_state (
                                        id integer PRIMARY KEY,
                                        timestamp     date    NOT NULL,
                                        """ + fds.LABEL_RS_RELAY_1 + """    integer     NOT NULL,
                                        """ + fds.LABEL_RS_RELAY_2 + """    integer     NOT NULL,
                                        """ + fds.LABEL_RS_RELAY_3 + """    integer     NOT NULL,
                                        synced    integer(1)  default 0
                                    ); """



# complete query

sql_create_mcu_table_complete = """ CREATE TABLE IF NOT EXISTS mcu (
                                        id          integer     PRIMARY KEY,
                                        timestamp   date        NOT NULL,
                                        """ + fds.LABEL_MCU_TEMP_1 + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_TEMP_2 + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_TEMP_3 + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_IN + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_OUT + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_MIDDLE + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_FLUX_IN + """        integer     NOT NULL,
                                        """ + fds.LABEL_MCU_FLUX_OUT + """        integer     NOT NULL,
                                        """ + fds.LABEL_MCU_CC_CURRENT + """           float       NOT NULL,
                                        """ + fds.LABEL_MCU_AC1_CURRENT + """          float       NOT NULL,
                                        """ + fds.LABEL_MCU_AC2_CURRENT + """          float       NOT NULL,
                                        """ + fds.LABEL_MCU_DHT11_AIR + """     float       NOT NULL,
                                        """ + fds.LABEL_MCU_DHT11_HUMIDITY + """      float       NOT NULL,
                                        """ + fds.LABEL_MCU_FLOODING_STATUS + """        integer     NOT NULL,
                                        """ + fds.LABEL_MCU_WATER_LEVEL + """    integer     NOT NULL,
                                        synced      integer(1)  default 0
                                    ); """


sql_create_mcu_table = """ CREATE TABLE IF NOT EXISTS mcu (
                                        id          integer     PRIMARY KEY,
                                        timestamp   date        NOT NULL,
                                        """ + fds.LABEL_MCU_TEMP_1 + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_TEMP_2 + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_IN + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_OUT + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_PRESSURE_MIDDLE + """        float       NOT NULL,
                                        """ + fds.LABEL_MCU_FLUX_IN + """        integer     NOT NULL,
                                        """ + fds.LABEL_MCU_FLUX_OUT + """        integer     NOT NULL,
                                        """ + fds.LABEL_MCU_CC_CURRENT + """           float       NOT NULL,
                                        """ + fds.LABEL_MCU_AC1_CURRENT + """          float       NOT NULL,
                                        """ + fds.LABEL_MCU_AC2_CURRENT + """          float       NOT NULL,
                                        synced      integer(1)  default 0
                                    ); """




### SQLITE QUERIES TO INSERT DATA

insert_mcu = """
            INSERT INTO mcu (
            id,
            """ + fds.LABEL_MCU_TEMP_1 + """ ,
            """ + fds.LABEL_MCU_TEMP_2 + """ ,
            """ + fds.LABEL_MCU_PRESSURE_IN + """ ,
            """ + fds.LABEL_MCU_PRESSURE_OUT + """ ,
            """ + fds.LABEL_MCU_PRESSURE_MIDDLE + """ ,
            """ + fds.LABEL_MCU_FLUX_IN + """ ,
            """ + fds.LABEL_MCU_FLUX_OUT + """ ,
            """ + fds.LABEL_MCU_CC_CURRENT + """ ,
            """ + fds.LABEL_MCU_AC1_CURRENT + """ ,
            """ + fds.LABEL_MCU_AC2_CURRENT + """ ,
            timestamp
        ) VALUES (
            NULL,
            :""" + fds.LABEL_MCU_TEMP_1 + """ ,
            :""" + fds.LABEL_MCU_TEMP_2 + """ ,
            :""" + fds.LABEL_MCU_PRESSURE_IN + """ ,
            :""" + fds.LABEL_MCU_PRESSURE_OUT + """ ,
            :""" + fds.LABEL_MCU_PRESSURE_MIDDLE + """ ,
            :""" + fds.LABEL_MCU_FLUX_IN + """ ,
            :""" + fds.LABEL_MCU_FLUX_OUT + """ ,
            :""" + fds.LABEL_MCU_CC_CURRENT + """ ,
            :""" + fds.LABEL_MCU_AC1_CURRENT + """ ,
            :""" + fds.LABEL_MCU_AC2_CURRENT + """ ,
            datetime('now')
        );
             """


insert_relay_box = """
            INSERT INTO relay_box (
              id,
              """ + fds.LABEL_RB_CH_ALARMS_3 + """ ,
              """ + fds.LABEL_RB_HOURMETER_LO + """ ,
              """ + fds.LABEL_RB_CH_FAULTS_1 + """ ,
              """ + fds.LABEL_RB_CH_ALARMS_1 + """ ,
              """ + fds.LABEL_RB_CH_FAULTS_3 + """ ,
              """ + fds.LABEL_RB_CH_FAULTS_2 + """ ,
              """ + fds.LABEL_RB_CH_ALARMS_4 + """ ,
              """ + fds.LABEL_RB_CH_FAULTS_4 + """ ,
              """ + fds.LABEL_RB_HOURMETER_HI + """ ,
              """ + fds.LABEL_RB_VB + """ ,
              """ + fds.LABEL_RB_ADC_VCH_4 + """ ,
              """ + fds.LABEL_RB_ADC_VCH_1 + """ ,
              """ + fds.LABEL_RB_ADC_VCH_2 + """ ,
              """ + fds.LABEL_RB_ADC_VCH_3 + """ ,
              """ + fds.LABEL_RB_T_MOD + """ ,
              """ + fds.LABEL_RB_GLOBAL_FAULTS + """ ,
              """ + fds.LABEL_RB_GLOBAL_ALARMS + """ ,
              """ + fds.LABEL_RB_CH_ALARMS_2 + """  ,
              timestamp
              )
            VALUES (
              NULL,
              :""" + fds.LABEL_RB_CH_ALARMS_3 + """ ,
              :""" + fds.LABEL_RB_HOURMETER_LO + """ ,
              :""" + fds.LABEL_RB_CH_FAULTS_1 + """ ,
              :""" + fds.LABEL_RB_CH_ALARMS_1 + """ ,
              :""" + fds.LABEL_RB_CH_FAULTS_3 + """ ,
              :""" + fds.LABEL_RB_CH_FAULTS_2 + """ ,
              :""" + fds.LABEL_RB_CH_ALARMS_4 + """ ,
              :""" + fds.LABEL_RB_CH_FAULTS_4 + """ ,
              :""" + fds.LABEL_RB_HOURMETER_HI + """ ,
              :""" + fds.LABEL_RB_VB + """ ,
              :""" + fds.LABEL_RB_ADC_VCH_4 + """ ,
              :""" + fds.LABEL_RB_ADC_VCH_1 + """ ,
              :""" + fds.LABEL_RB_ADC_VCH_2 + """ ,
              :""" + fds.LABEL_RB_ADC_VCH_3 + """ ,
              :""" + fds.LABEL_RB_T_MOD + """ ,
              :""" + fds.LABEL_RB_GLOBAL_FAULTS + """ ,
              :""" + fds.LABEL_RB_GLOBAL_ALARMS + """ ,
              :""" + fds.LABEL_RB_CH_ALARMS_2 + """ ,
              datetime('now')
              );
            """

insert_charge_controller = """
            INSERT INTO charge_controller (
               id,
               """ + fds.LABEL_CC_OUT_POWER + """ ,
               """ + fds.LABEL_CC_MINTB_DAILY + """ ,
               """ + fds.LABEL_CC_DIPSWITCHES + """ ,
               """ + fds.LABEL_CC_ARRAY_V + """ ,
               """ + fds.LABEL_CC_MINVB_DAILY + """ ,
               """ + fds.LABEL_CC_ARRAY_I + """ ,
               """ + fds.LABEL_CC_BATT_SENSED_V + """,
               """ + fds.LABEL_CC_STATENUM + """ ,
               """ + fds.LABEL_CC_MAXTB_DAILY + """ ,
               """ + fds.LABEL_CC_BATTS_I + """ ,
               """ + fds.LABEL_CC_BATTS_V + """,
               """ + fds.LABEL_CC_RTS_TEMP + """ ,
               """ + fds.LABEL_CC_IN_POWER + """ ,
               """ + fds.LABEL_CC_MAXVB_DAILY + """ ,
               """ + fds.LABEL_CC_HS_TEMP + """ ,
               timestamp
               )
            VALUES (
              NULL,
              :""" + fds.LABEL_CC_OUT_POWER + """ ,
              :""" + fds.LABEL_CC_MINTB_DAILY + """ ,
              :""" + fds.LABEL_CC_DIPSWITCHES + """ ,
              :""" + fds.LABEL_CC_ARRAY_V + """ ,
              :""" + fds.LABEL_CC_MINVB_DAILY + """ ,
              :""" + fds.LABEL_CC_ARRAY_I + """ ,
              :""" + fds.LABEL_CC_BATT_SENSED_V + """,
              :""" + fds.LABEL_CC_STATENUM + """ ,
              :""" + fds.LABEL_CC_MAXTB_DAILY + """ ,
              :""" + fds.LABEL_CC_BATTS_I + """ ,
              :""" + fds.LABEL_CC_BATTS_V + """,
              :""" + fds.LABEL_CC_RTS_TEMP + """ ,
              :""" + fds.LABEL_CC_IN_POWER + """ ,
              :""" + fds.LABEL_CC_MAXVB_DAILY + """ ,
              :""" + fds.LABEL_CC_HS_TEMP + """ ,
              datetime('now')
              );
            """

insert_relay_state = """
                     INSERT INTO relay_state (
                        id,
                        """ + fds.LABEL_RS_RELAY_1 + """ ,
                        """ + fds.LABEL_RS_RELAY_2 + """ ,
                        """ + fds.LABEL_RS_RELAY_3 + """ ,
                        timestamp
                        )
                     VALUES (
                        NULL,
                        :""" + fds.LABEL_RS_RELAY_1 + """ ,
                        :""" + fds.LABEL_RS_RELAY_2 + """ ,
                        :""" + fds.LABEL_RS_RELAY_3 + """ ,
                        datetime('now')
                        );
                     """
