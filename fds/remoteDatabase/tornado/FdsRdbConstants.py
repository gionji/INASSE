
SQLITE_FILENAME = './DB_fds_offgridbox.sqlite'


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




### SQLITE QUERIES TO INSERT DATA

remote_insert_mcu = """
		INSERT INTO mcu (
			id,
                        boardId, 
                        syncTime,
			temp1,
			temp2,
			pres1,
			pres2,
			pres3,
                        flux1,
			flux2,
			cc,
			ac1,
                        ac2,
                        timestamp
		) VALUES (
			NULL,
			:boardId, 
                        datetime('now'),
                        :temp1,
			:temp2,
			:pres1,
			:pres2,
			:pres3,
			:flux1,
			:flux2,
			:cc,
			:ac1,
			:ac2,
			:timestamp
		);
             """


remote_insert_relay_box = """
            INSERT INTO relay_box (
              id,
              boardId, syncTime,
              ch_alarms_3, hourmeter_LO,
              ch_faults_1, ch_alarms_1,
              ch_faults_3, ch_faults_2, ch_alarms_4, ch_faults_4, hourmeter_HI,
              adc_vb, adc_vch_4, adc_vch_1, adc_vch_2, adc_vch_3,
              t_mod, global_faults, global_alarms, ch_alarms_2 , timestamp
              )
            VALUES (
              NULL,
              :boardId, datetime('now'),
              :ch_alarms_3, :hourmeter_LO, :ch_faults_1, :ch_alarms_1,
              :ch_faults_3, :ch_faults_2, :ch_alarms_4, :ch_faults_4, :hourmeter_HI,
              :adc_vb, :adc_vch_4, :adc_vch_1, :adc_vch_2, :adc_vch_3,
              :t_mod, :global_faults, :global_alarms, :ch_alarms_2, :timestamp
              );
            """

remote_insert_charge_controller = """
            INSERT INTO charge_controller (
               id,
               boardId, syncTime,
               outPower, minTb_daily, dipswitches,
               arrayV, minVb_daily, arrayI, battsSensedV,
               statenum, maxTb_daily, battsI, battsV, rtsTemp,
               inPower, maxVb_daily, hsTemp, timestamp
               )
            VALUES (
              NULL,
              :boardId, datetime('now'),
              :outPower, :minTb_daily, :dipswitches,
              :arrayV, :minVb_daily, :arrayI, :battsSensedV,
              :statenum, :maxTb_daily, :battsI, :battsV, :rtsTemp,
              :inPower, :maxVb_daily, :hsTemp, :timestamp
              );
            """

remote_insert_relay_state = """
                     INSERT INTO relay_state (
                        id,
                        boardId, syncTime,
                        relay_1, relay_2, relay_3, timestamp
                        )
                     VALUES (
                        NULL,
                        :boardId, datetime('now'),
                        :relay_1, :relay_2, :relay_3, :timestamp
                        );
                     """
