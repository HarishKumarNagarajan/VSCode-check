def create_report(date,report_name):
    try:
        import pyodbc
        import xlsxwriter
    except:
        return {'Description':'Module Error','Status':False}


    try:
        
        #date = '2019-10-15'
        base_url = 'http://neodevqa01.southindia.cloudapp.azure.com:26062/'
        log_image = 'data/log_images/'
        attendance_image = 'data/attendance_images/'
        #report_name='final_report.xlsx'
        """
        conn_str = (
                    r'Driver={SQL Server};'
                    r'Server=LNJAGDISH;'
                    r'Database=MCLG_LIVE_TMA_Report;'
                    r'Trusted_Connection=yes;'
                    )
        """
        conn_str ="DRIVER={SQL SERVER};server=NEO-DEV-QA-01\SQLEXPRESS;database=MCLG_LIVE_Aug1;uid=sa;pwd=neo-dev-qa-01"

        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()

        def quer_trainer(date):
            quer_trainer = '''
                
                SELECT DISTINCT
                                        T.trainer_name,
                                        L.trainer_email
                        FROM	        [tma].[tbl_trainer_stage_log] AS L
                        LEFT JOIN	[tma].[tbl_trainers] AS T ON T.trainer_email=L.trainer_email
                        WHERE		CAST(L.log_date_time AS DATE)=CAST('{}' AS DATE)
                        ORDER BY        trainer_name
            '''.format(date)
            return quer_trainer

        def quer_batch(date,trainer_email):
            quer_batch = '''
                SELECT		DISTINCT 
                                                    L.batch_id,
                                                    B.batch_code,
                                                    B.batch_start_date,
                                                    B.batch_end_date,
                                                    B.customer_name,
                                                    B.center_name,
                                                    B.center_type,
                                                    B.business_unit,
                                                    B.course_code,
                                                    B.course_name
                                        FROM		[tma].[tbl_trainer_stage_log] AS L
                                        LEFT JOIN	[tma].[tbl_trainers] AS T ON T.trainer_email=L.trainer_email
                                        LEFT JOIN	[tma].[tbl_batches] AS B ON B.batch_id=L.batch_id
                                        WHERE		CAST(L.log_date_time AS DATE)=CAST('{}' AS DATE)
                                        AND			L.trainer_email='{}'
                                        ORDER BY    batch_code
            '''.format(date,trainer_email)
            #  (date,data_trainer[0][1])
            return quer_batch




        def quer_session(date,trainer_email,batch_id):
            quer_session = '''
                        SELECT	    DISTINCT
                                                            L.session_id,
                                                            S.session_name,
                                                            FORMAT(L.log_date_time,'dd-MMM-yyyy') AS log_date
                                                FROM		[tma].[tbl_trainer_stage_log] AS L
                                                LEFT JOIN	[tma].[tbl_sessions] AS S ON S.session_id=L.session_id
                                                WHERE		CAST(L.log_date_time AS DATE)=CAST('{}' AS DATE)
                                                AND		L.trainer_email='{}'
                                                AND		L.batch_id={}
                                                ORDER BY    session_id
                        '''.format(date,trainer_email,batch_id)
            return quer_session


        def quer_stage(trainer_email, batch_id,session_id):
            quer_attendance = '''
                                                        WITH TL AS
                                                        (
                                                            SELECT	
                                                                        '{}' AS trainer_email,
                                                                        '{}' AS batch_id,
                                                                        '{}' AS session_id
                                                            
                                                        )
                                                        SELECT	    FORMAT(STG1.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage1_log_time,
                                                                    STG1.image_file_name AS stage1_log_image,
                                                                    ('https://www.google.com/maps/search/?api=1&query='+STG1.latitude+','+STG1.longitude) AS stage1_location,
                                                                    FORMAT(STG2.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage2_log_time,
                                                                    STG2.image_file_name AS stage2_log_image,
                                                                    ('https://www.google.com/maps/search/?api=1&query='+STG2.latitude+','+STG2.longitude) AS stage2_location,
                                                                    FORMAT(STG3.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage3_log_time,
                                                                    STG3.image_file_name AS stage3_log_image,
                                                                    ('https://www.google.com/maps/search/?api=1&query='+STG3.latitude+','+STG3.longitude) AS stage3_location,
                                                                    FORMAT(STG4.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage4_log_time,
                                                                    STG4.image_file_name AS stage4_log_image,
                                                                    ('https://www.google.com/maps/search/?api=1&query='+STG4.latitude+','+STG4.longitude) AS stage4_location
                                                        FROM		TL	
                                                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG1 ON STG1.trainer_email=TL.trainer_email AND STG1.batch_id=TL.batch_id AND STG1.session_id=TL.session_id AND STG1.stage_id=1
                                                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG2 ON STG2.trainer_email=TL.trainer_email AND STG2.batch_id=TL.batch_id AND STG2.session_id=TL.session_id AND STG2.stage_id=2
                                                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG3 ON STG3.trainer_email=TL.trainer_email AND STG3.batch_id=TL.batch_id AND STG3.session_id=TL.session_id AND STG3.stage_id=3
                                                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG4 ON STG4.trainer_email=TL.trainer_email AND STG4.batch_id=TL.batch_id AND STG4.session_id=TL.session_id AND STG4.stage_id=4
                        '''.format(trainer_email, batch_id,session_id)
            return quer_attendance

            
        def quer_candidate(date,trainer_email,batch_id):
            quer_candidate = '''
                SELECT		DISTINCT
                                                                C.candidate_name,
                                                                C.enrollment_id
                                                    FROM		[tma].[tbl_trainer_stage_log] AS L
                                                    LEFT JOIN	[tma].[tbl_batches] AS B ON B.batch_id=L.batch_id
                                                    LEFT JOIN	[tma].[tbl_candidates] AS C ON C.batch_code=B.batch_code
                                                    WHERE		CAST(L.log_date_time AS DATE)=CAST('{}' AS DATE)
                                                    AND			L.trainer_email='{}'
                                                    AND			L.batch_id='{}'
                                                    ORDER BY    candidate_name
            '''.format(date,trainer_email,batch_id)
            # date,data_trainer[0][1],data_batch[0][0]
            return quer_candidate

        def quer_attendance(batch_id,session_id,enrollment_id):
            quer_attendance = '''
                                                                    WITH AD AS
                            
                                                                    (
                                                                        SELECT		CAST(A.[key] AS bigint) AS enrollment_id,
                                                                                    REPLACE(CONVERT(VARCHAR,ATT.attendance_date,106),' ','-') AS attendance_date,
                                                                                    ISNULL(NULLIF(A.[value],''),'NA') AS image_file_name
                                                                        FROM		tma.tbl_candidate_attendance AS ATT
                                                                        CROSS APPLY OPENJSON(ATT.attendance_json_data) AS A
                                                                        WHERE       ATT.batch_id='{}'
                                                                        AND         ATT.session_id='{}'
                                                                    )
                                                                    SELECT	CASE WHEN ISNULL(AD.enrollment_id,'')<>'' THEN 'Present' ELSE 'Absent' END AS attendance,
                                                                            AD.attendance_date,
                                                                            CASE AD.image_file_name 
                                                                                WHEN 'NA' THEN 'NA' 
                                                                                ELSE AD.image_file_name 
                                                                            END AS image_file_name
                                                                    FROM    AD 
                                                                    WHERE   AD.enrollment_id='{}'

                        '''.format(batch_id,session_id,enrollment_id)
            #data_batch[0][0],data_session[0][0],data_candidate[0][1]
            return quer_attendance

        def quer_attendance_1(batch_id,session_id):
            quer_attendance = '''
                                                            WITH AD AS
                                                            (
                                                                SELECT	    A.[key] AS image_file_name,
                                                                            A.[value] AS remarks
                                                                FROM	    tma.tbl_candidate_attendance AS ATT
                                                                CROSS APPLY OPENJSON(ISNULL(NULLIF(ATT.group_attendance_image_json_data,''),'{}')) AS A
                                                                ''' + '''
                                                                WHERE       ATT.batch_id={}
                                                                AND         ATT.session_id={}
                                                            )
                                                            SELECT	CASE ISNULL(AD.image_file_name,'') 
                                                                        WHEN '' THEN 'NA' 
                                                                        ELSE AD.image_file_name
                                                                    END AS image_file_name,
                                                                    AD.remarks
                                                            FROM    AD
                        '''.format(batch_id,session_id)
            #data_batch[0][0],data_session[0][0],data_candidate[0][1]
            return quer_attendance


        ###############################################################
        
        workbook = xlsxwriter.Workbook(report_name)
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})

        merge_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top'})
            #'fg_color': 'yellow'
            #'bold': 1,

        write_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top'})
            #'fg_color': 'yellow'
        url_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top',
            'font_color': 'blue',
            'underline': 1})
            


        worksheet = workbook.add_worksheet('Stage Log')
        default_column = ['TRAINER NAME', 'TRAINER EMAIL', 'BATCH ID', 'BATCH CODE', 'BATCH START DATE',
                          'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'BUSSINESS UNIT',
                          'COURSE CODE', 'COURSE NAME', 'SESSION ID', 'SESSION NAME', 'ATTENDANCE DATE']
        second_row = ['LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION',
                  'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION', 'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION',
                  'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION']
        first_row = ['SESSION START', 'ONGOING SESSION', 'MARK ATTENDANCE', 'SESSION COMPLETED']

        for col_num, value in enumerate(default_column):
            worksheet.merge_range(0, col_num, 1, col_num, value, header_format)

        # Write the column headers with the defined format.
        for col_num, value in enumerate(second_row):
            worksheet.write(1, 15+col_num, value, header_format)

        for col_num, value in enumerate(first_row):
            worksheet.merge_range(0, 15+col_num*3, 0, 17+col_num*3, value, header_format)



        row=1;
        session_row = 2
        batch_row = 2
        trainer_row = 2

        curs.execute(quer_trainer(date))
        data_trainer = curs.fetchall()


        for trainer in data_trainer:
            temp = list(trainer)
            
            curs.execute(quer_batch(date,trainer[1]))
            data_batch = curs.fetchall()

            for batch in data_batch:

                curs.execute(quer_session(date,trainer[1],batch[0]))
                data_session = curs.fetchall()
                
                for session in data_session:

                    curs.execute(quer_stage(trainer[1], batch[0], session[0]))
                    data_stage = curs.fetchall()[0]
                    
                    
                    row += 1
                    #print('1', trainer, batch, session)

                    worksheet.write(row,12,session[0],write_format)
                    worksheet.write(row,13,session[1],write_format)
                    worksheet.write(row,14,session[2],write_format)
                    #print(len(data_attendance))
                    worksheet.write(row,15,'NA',write_format) if data_stage[0] == None else worksheet.write(row,15,data_stage[0],write_format)
                    worksheet.write(row,16,'NA',write_format) if data_stage[1] == None else worksheet.write_url(row, 16, base_url + log_image + data_stage[1],  url_format, string='Image', tip='Click to open image')
                    worksheet.write(row,17,'NA',write_format) if data_stage[2] == None else worksheet.write_url(row, 17, data_stage[2],  url_format, string='Location', tip='Click to open in MAP')
                    worksheet.write(row,18,'NA',write_format) if data_stage[3] == None else worksheet.write(row,18,data_stage[3],write_format)
                    worksheet.write(row,19,'NA',write_format) if data_stage[4] == None else worksheet.write_url(row, 19, base_url + log_image + data_stage[4],  url_format, string='Image', tip='Click to open image')
                    worksheet.write(row,20,'NA',write_format) if data_stage[5] == None else worksheet.write_url(row, 20, data_stage[5],  url_format, string='Location', tip='Click to open in MAP')
                    worksheet.write(row,21,'NA',write_format) if data_stage[6] == None else worksheet.write(row,21,data_stage[6],write_format)
                    worksheet.write(row,22,'NA',write_format) if data_stage[7] == None else worksheet.write_url(row, 22, base_url + log_image + data_stage[7],  url_format, string='Image', tip='Click to open image')
                    worksheet.write(row,23,'NA',write_format) if data_stage[8] == None else worksheet.write_url(row, 23, data_stage[8],  url_format, string='Location', tip='Click to open in MAP')
                    worksheet.write(row,24,'NA',write_format) if data_stage[9] == None else worksheet.write(row,24,data_stage[9],write_format)
                    worksheet.write(row,25,'NA',write_format) if data_stage[10] == None else worksheet.write_url(row, 25, base_url + log_image + data_stage[10],  url_format, string='Image', tip='Click to open image')
                    worksheet.write(row,26,'NA',write_format) if data_stage[11] == None else worksheet.write_url(row, 26, data_stage[11],  url_format, string='Location', tip='Click to open in MAP')
                    
                            
                            

                    if session_row<row:
                        worksheet.merge_range(session_row, 12, row, 12, session[0], merge_format )
                        worksheet.merge_range(session_row, 13, row, 13, session[1], merge_format )
                        worksheet.merge_range(session_row, 14, row, 14, session[2], merge_format )
                    else:
                        worksheet.write(row, 12, session[0],write_format)
                        worksheet.write(row, 13, session[1],write_format)
                        worksheet.write(row, 14, session[2],write_format)
                        
                    session_row = row+1
                    
                if batch_row<row:
                    worksheet.merge_range(batch_row, 2, row, 2, batch[0], merge_format)
                    worksheet.merge_range(batch_row, 3, row, 3, batch[1], merge_format)
                    worksheet.merge_range(batch_row, 4, row, 4, batch[2], merge_format)
                    worksheet.merge_range(batch_row, 5, row, 5, batch[3], merge_format)
                    worksheet.merge_range(batch_row, 6, row, 6, batch[4], merge_format)
                    worksheet.merge_range(batch_row, 7, row, 7, batch[5], merge_format)
                    worksheet.merge_range(batch_row, 8, row, 8, batch[6], merge_format)
                    worksheet.merge_range(batch_row, 9, row, 9, batch[7], merge_format)
                    worksheet.merge_range(batch_row, 10, row, 10, batch[8], merge_format)
                    worksheet.merge_range(batch_row, 11, row, 11, batch[9], merge_format)
                else:
                    worksheet.write(row, 2, batch[0],write_format)
                    worksheet.write(row, 3, batch[1],write_format)
                    worksheet.write(row, 4, batch[2],write_format)
                    worksheet.write(row, 5, batch[3],write_format)
                    worksheet.write(row, 6, batch[4],write_format)
                    worksheet.write(row, 7, batch[5],write_format)
                    worksheet.write(row, 8, batch[6],write_format)
                    worksheet.write(row, 9, batch[7],write_format)
                    worksheet.write(row, 10, batch[8],write_format)
                    worksheet.write(row, 11, batch[9],write_format)
                    
                    
                
                batch_row = row+1

            if trainer_row<row:
                worksheet.merge_range(trainer_row, 0, row, 0, trainer[0], merge_format)
                worksheet.merge_range(trainer_row, 1, row, 1, trainer[1], merge_format)
            else:
                worksheet.write(row,0,trainer[0],write_format)
                worksheet.write(row,1,trainer[1],write_format)

            trainer_row = row+1
            
                    
        worksheet = workbook.add_worksheet('Candidate Attendance')
        default_column = ['TRAINER NAME', 'TRAINER EMAIL', 'BATCH ID', 'BATCH CODE', 'BATCH START DATE',
                          'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'BUSSINESS UNIT',
                          'COURSE CODE', 'COURSE NAME', 'SESSION ID', 'SESSION NAME', 'LOG DATE', 'CANDIDATE NAME', 'ENROLLMENT ID',
                          'ATTENDANCE', 'ATTENDANCE DATE', 'ATTENDANCE IMAGE']

        for col_num, value in enumerate(default_column):
            worksheet.write(0, col_num, value, header_format)

        row=0;
        session_row = 1
        batch_row = 1
        trainer_row = 1

        for trainer in data_trainer:
            temp = list(trainer)
            
            curs.execute(quer_batch(date,trainer[1]))
            data_batch = curs.fetchall()

            for batch in data_batch:

                curs.execute(quer_candidate(date,trainer[1],batch[0]))
                data_candidate = curs.fetchall()

                curs.execute(quer_session(date,trainer[1],batch[0]))
                data_session = curs.fetchall()
                
                for session in data_session:

                    for candidate in data_candidate:
                        #print('2',trainer, batch, session, candidate)
                        if candidate[1]==None:
                            row += 1
                            worksheet.write(row,15,'NA', write_format)
                            worksheet.write(row,16,'NA', write_format)
                            worksheet.write(row,17,'NA', write_format)
                            worksheet.write(row,18,'NA', write_format)
                            worksheet.write(row,19,'NA', write_format)

                        else:
                            curs.execute(quer_attendance(batch[0],session[0],candidate[1]))
                            data_attendance = curs.fetchall()

                            data = list(trainer) + list(batch) + list(session) + list(candidate)

                            row += 1
                            worksheet.write(row,15,candidate[0], write_format)
                            worksheet.write(row,16,candidate[1], write_format)
                            if len(data_attendance)>0:
                                attendance = data_attendance[0]
                                worksheet.write(row,17,attendance[0], write_format)
                                worksheet.write(row,18,attendance[1], write_format)
                                worksheet.write(row,19,attendance[2], write_format)
                            else:
                                worksheet.write(row,17,'NA', write_format)
                                worksheet.write(row,18,'NA', write_format)
                                worksheet.write(row,19,'NA', write_format)
                                

                    if session_row<row:
                        worksheet.merge_range(session_row, 12, row, 12, session[0], merge_format )
                        worksheet.merge_range(session_row, 13, row, 13, session[1], merge_format )
                        worksheet.merge_range(session_row, 14, row, 14, session[2], merge_format )
                    else:
                        worksheet.write(row, 12, session[0],write_format)
                        worksheet.write(row, 13, session[1],write_format)
                        worksheet.write(row, 14, session[2],write_format)
                        
                    session_row = row+1
                    
                if batch_row<row:
                    worksheet.merge_range(batch_row, 2, row, 2, batch[0], merge_format)
                    worksheet.merge_range(batch_row, 3, row, 3, batch[1], merge_format)
                    worksheet.merge_range(batch_row, 4, row, 4, batch[2], merge_format)
                    worksheet.merge_range(batch_row, 5, row, 5, batch[3], merge_format)
                    worksheet.merge_range(batch_row, 6, row, 6, batch[4], merge_format)
                    worksheet.merge_range(batch_row, 7, row, 7, batch[5], merge_format)
                    worksheet.merge_range(batch_row, 8, row, 8, batch[6], merge_format)
                    worksheet.merge_range(batch_row, 9, row, 9, batch[7], merge_format)
                    worksheet.merge_range(batch_row, 10, row, 10, batch[8], merge_format)
                    worksheet.merge_range(batch_row, 11, row, 11, batch[9], merge_format)
                else:
                    worksheet.write(row, 2, batch[0],write_format)
                    worksheet.write(row, 3, batch[1],write_format)
                    worksheet.write(row, 4, batch[2],write_format)
                    worksheet.write(row, 5, batch[3],write_format)
                    worksheet.write(row, 6, batch[4],write_format)
                    worksheet.write(row, 7, batch[5],write_format)
                    worksheet.write(row, 8, batch[6],write_format)
                    worksheet.write(row, 9, batch[7],write_format)
                    worksheet.write(row, 10, batch[8],write_format)
                    worksheet.write(row, 11, batch[9],write_format)
                    
                    
                
                batch_row = row+1

            if trainer_row<row:
                worksheet.merge_range(trainer_row, 0, row, 0, trainer[0], merge_format)
                worksheet.merge_range(trainer_row, 1, row, 1, trainer[1], merge_format)
            else:
                worksheet.write(row,0,trainer[0], write_format)
                worksheet.write(row,1,trainer[1], write_format)

            trainer_row = row+1
            

        worksheet = workbook.add_worksheet('Session Group Images')
        default_column = ['TRAINER NAME', 'TRAINER EMAIL', 'BATCH ID', 'BATCH CODE', 'BATCH START DATE',
                          'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'BUSSINESS UNIT',
                          'COURSE CODE', 'COURSE NAME', 'SESSION ID', 'SESSION NAME', 'ATTENDANCE DATE', 'IMAGE', 'FLAG']

        # Write the column headers with the defined format.
        for col_num, value in enumerate(default_column):
            worksheet.write(0, col_num, value, header_format)
        row=0;
        session_row = 1
        batch_row = 1
        trainer_row = 1

        for trainer in data_trainer:
            temp = list(trainer)
            
            curs.execute(quer_batch(date,trainer[1]))
            data_batch = curs.fetchall()

            for batch in data_batch:

                curs.execute(quer_session(date,trainer[1],batch[0]))
                data_session = curs.fetchall()
                
                for session in data_session:

                    curs.execute(quer_attendance_1(batch[0], session[0]))
                    data_attendance = curs.fetchall()
                    
                    #print('3',trainer, batch, session)
                    row += 1

                    worksheet.write(row,12,session[0])
                    worksheet.write(row,13,session[1])
                    worksheet.write(row,14,session[2])
                    if len(data_attendance)>0:
                        worksheet.write_url(row, 15, base_url + attendance_image + data_attendance[0][0], url_format, string='Image', tip='Click to open image')
                        worksheet.write(row,16,data_attendance[0][1],write_format)
                        
                    else:
                        worksheet.write(row,15,'NA', write_format)
                        worksheet.write(row,16,'NA', write_format)
                    
                    if session_row<row:
                        worksheet.merge_range(session_row, 12, row, 12, session[0], merge_format )
                        worksheet.merge_range(session_row, 13, row, 13, session[1], merge_format )
                        worksheet.merge_range(session_row, 14, row, 14, session[2], merge_format )
                    else:
                        worksheet.write(row, 12, session[0],write_format)
                        worksheet.write(row, 13, session[1],write_format)
                        worksheet.write(row, 14, session[2],write_format)
                       
                    session_row = row+1
                    
                if batch_row<row:
                    worksheet.merge_range(batch_row, 2, row, 2, batch[0], merge_format)
                    worksheet.merge_range(batch_row, 3, row, 3, batch[1], merge_format)
                    worksheet.merge_range(batch_row, 4, row, 4, batch[2], merge_format)
                    worksheet.merge_range(batch_row, 5, row, 5, batch[3], merge_format)
                    worksheet.merge_range(batch_row, 6, row, 6, batch[4], merge_format)
                    worksheet.merge_range(batch_row, 7, row, 7, batch[5], merge_format)
                    worksheet.merge_range(batch_row, 8, row, 8, batch[6], merge_format)
                    worksheet.merge_range(batch_row, 9, row, 9, batch[7], merge_format)
                    worksheet.merge_range(batch_row, 10, row, 10, batch[8], merge_format)
                    worksheet.merge_range(batch_row, 11, row, 11, batch[9], merge_format)
                else:
                    worksheet.write(row, 2, batch[0],write_format)
                    worksheet.write(row, 3, batch[1],write_format)
                    worksheet.write(row, 4, batch[2],write_format)
                    worksheet.write(row, 5, batch[3],write_format)
                    worksheet.write(row, 6, batch[4],write_format)
                    worksheet.write(row, 7, batch[5],write_format)
                    worksheet.write(row, 8, batch[6],write_format)
                    worksheet.write(row, 9, batch[7],write_format)
                    worksheet.write(row, 10, batch[8],write_format)
                    worksheet.write(row, 11, batch[9],write_format)
                    
                    
                
                batch_row = row+1

            if trainer_row<row:
                worksheet.merge_range(trainer_row, 0, row, 0, trainer[0], merge_format)
                worksheet.merge_range(trainer_row, 1, row, 1, trainer[1], merge_format)
            else:
                worksheet.write(row,0,trainer[0], write_format)
                worksheet.write(row,1,trainer[1], write_format)

            trainer_row = row+1
            
                    
                            
        workbook.close()
        return {'Report Name':report_name,'Status':True}
    except Exception as e:
        return {'Description':'Not able to create file becuase of '+str(e),'Status':False}
