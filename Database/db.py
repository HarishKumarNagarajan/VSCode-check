import pyodbc
from .config import *
import pandas as pd

class Database:
    def Login(email,passw):
        tr =[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("SELECT u.user_id,u.user_name,u.user_role_id FROM users.tbl_users AS u LEFT JOIN users.tbl_user_details AS ud ON ud.user_id=u.user_id where ud.email='"+email+"' AND u.password='"+passw+"';")
        for row in cur:
            tr.append(row)
        cur.close()
        con.close()
        return tr
    def practicebasedonuser(user_id):
        prac = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_practice_course_neo] ?, ?'
        values = (user_id,None)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
            prac.append(h)
        cur.close()
        con.close()
        practiceforuser={'Pratices': prac}
        print(practiceforuser)
        return practiceforuser
    def CourseBasedOnUserPractice(user_id,practice_id):
        courses =[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_practice_course_neo] ?, ?'
        values = (user_id,practice_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        lent=0
        for row in cur:
            courseid = row[4].split (",")
            coursename = row[5].split (",")
            lent=len(row)
        for i in range(0,lent):
            h = { 'Course_Id': courseid[i], 'Course_Name':coursename[i]}
            courses.append(h)
        cur.close()
        con.close()
        courseforuserpractice={'Courses': courses}
        return courseforuserpractice
    def report_table_db(user_id, practice_id, course_id, date_from, date_to):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        # curs.execute("select * from [masters].[tbl_courses] where course_id='{}'".format(course))
        # course_id = curs.fetchall()[0][0]
        
        # curs.execute("select * from [masters].[tbl_practice] where practice_id='{}'".format(practice))
        # practice_id = curs.fetchall()[0][0]
        
        

        quer = "call [candidate_details].[sp_candidate_report]({},{},{},'{}','{}')".format(user_id, practice_id, course_id, date_from, date_to)
        quer = "{"+ quer + "}"
        
        curs.execute(quer)
        #data = curs.fetchall()
        data=[]
        for row in curs:
            h=[]
            for i in range(0,len(row)):
                v=row[i]
                h.append(v)
            data.append(h)
        ind=[]
        cl = ['candidate_id','candidate_name','candidate_mobile_number','date_of_join','mobilizer_name','workflow_id','practice_id','practice_name','course_id','course_name','center_id','center_name','section_id','section_name','section_completion_date','question_id','question_text','response','section_result','registration_id','enrollment_id']
        for i in range(0,len(data)):
            ind.append(i)
        #print(pd.DataFrame(data,columns=cl))
        df = pd.DataFrame(data,columns=cl)
        column_req=['candidate_name','candidate_mobile_number','date_of_join','mobilizer_name','practice_name','course_name','center_name','section_name','section_completion_date','question_text','response','section_result','registration_id','enrollment_id']
        df= df[column_req]
        df.columns = ['Candidate_Name','Candidate_Mobile_Number','Date_Of_Join','Mobilizer_Name','Practice_Name','Course_Name','Center_Name','Section_Name','Section_Completion_Date','Question_Text','Response','Section_Result','Registration_Id','Enrollment_Id']
        curs.close()
        con.close()
        return df


    def center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_center_types_list] ?, ?, ?, ?, ?, ?'
        values = (center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        #global count
        #count = count + 1
        return content

    def add_center_type_details(center_type_name,user_id,is_active,center_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_center_types ?, ?, ?, ?'
        values = (center_type_id,center_type_name,user_id,is_active)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_center_type_details(glob_center_type_id):
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        sql = 'SELECT * FROM [masters].[tbl_center_type] where center_type_id=?'
        values = (glob_center_type_id)
        
        cur.execute(sql,(values))
        
        columns = [column[0].title() for column in cur.description]
        
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        
        cur.close()
        con.close()
        return h

    def center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_center_category_list] ?, ?, ?, ?, ?, ?'
        values = (center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_center_category_details(center_category_name,user_id,is_active,center_category_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_center_categories ?, ?, ?, ?'
        values = (center_category_id,center_category_name,user_id,is_active)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_center_category_details(glob_center_category_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_center_category] where center_category_id=?'
        values = (glob_center_category_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h
    def center_list(center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_centers_list] ?, ?, ?, ?, ?, ?'
        values = (center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[20]
            fil=row[19]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_center_details(center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_centers] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name)
        print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def GetCenter(glob_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_center] where center_id=?'
        values = (glob_center_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13]}
        cur.close()
        con.close()
        return h
    def GetCenterType():
        center_type = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_center_types] @center_type_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center_type.append(h)
        cur2.close()
        con.close()
        return center_type
    def GetCenterCategory():
        center_cat = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_center_categories] @center_category_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center_cat.append(h)
        cur2.close()
        con.close()
        return center_cat
    def get_all_BU():
        bu = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_bu] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            bu.append(h)
        cur.close()
        con.close()
        return bu
    def get_all_Cluster_Based_On_Region(region_id):
        cluster = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_cluster] where is_active=1 AND region_id=?;'
        values=(region_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            cluster.append(h)
        cur.close()
        con.close()
        print(cluster)
        return cluster
    def GetCountry():
        countries = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM [masters].[tbl_countries]")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            countries.append(h)
        cur2.close()
        con.close()
        return countries
    def GetStatesBasedOnCountry(country_id):
        states = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC	[masters].[sp_get_all_states_based_on_country] @country_id = "+country_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            states.append(h)
        cur2.close()
        con.close()
        return states
    def GetDistrictsBasedOnStates(state_id):
        districts = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC	[masters].[sp_get_all_districts_based_on_state] @state_id = "+state_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            districts.append(h)
        cur2.close()
        con.close()
        return districts

    def course_list(course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_list] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[10]
            fil=row[9]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def GetPractice():
        practice = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("EXEC [masters].[sp_get_all_practices] @practice_id = NULL;")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            practice.append(h)
        cur.close()
        con.close()
        return practice
    def GetProjectBasedOnPractice(project_id,practice_id):
        projects = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql="EXEC [masters].[sp_get_projects_based_on_practice] ?, ?;"
        values=(project_id,practice_id)
        cur.execute(sql, (values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            projects.append(h)
        cur.close()
        con.close()
        return projects
    def GetAllCenter():
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_centers] @center_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def add_course_details(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_course] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_course_details(glob_course_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_detail] ?'
        values = (glob_course_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    def get_qp_course():
        qp = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT qp.qp_id,qp.qp_name FROM masters.tbl_qp AS qp where is_active=1")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            qp.append(h)
        cur2.close()
        con.close()
        return qp
        
    
    def user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_user_role_list] ?, ?, ?, ?, ?, ?'
        values = (user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_user_role_details(user_role_name,user_id,is_active,user_role_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_user_role] ?, ?, ?, ?'
        values = (user_role_name,user_id,is_active,user_role_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_user_role_details(glob_user_role_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [users].[tbl_user_role] where user_role_id=?'
        values = (glob_user_role_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h    
    def user_list(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_users_list] ?, ?, ?, ?, ?, ?'
        values = (user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[12]
            fil=row[11]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_user_details(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_users] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        if center_ids == None:
            values = (user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,"",is_reporting_manager)
        else:
            values = (user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
            UserId=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated" , "UserId": UserId}
        else: 
            if pop==0:
                msg={"message":"Created", "UserId": UserId}
            else:
                if pop==2:
                    msg={"message":"User with the Unique fields already exists", "UserId": UserId}
        return msg
    def GetUserRole():
        userrole = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("Select * from users.tbl_user_role where is_active=1;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            userrole.append(h)
        cur2.close()
        con.close()
        return userrole
    def get_user_details(glob_user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'EXEC	[users].[sp_get_user_details] @user_id = ?'
        values = (glob_user_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7]}
        cur.close()
        con.close()
        return h
    def batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_get_batch_list] ?, ?, ?, ?, ?, ?'
        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[19]
            fil=row[18]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_batch_details(batch_id,batch_name,course_id,batch_code,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active,actual_start_date,actual_end_date):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	batches.sp_add_edit_batches ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active,batch_code,actual_start_date,actual_end_date)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","batch_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","batch_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Batch with the Batch code already exists","batch_flag":2}
        return msg
    def get_batch_details(glob_batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [batches].[tbl_batches] where batch_id=?'
        values = (glob_batch_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18],""+columns[19]+"":row[19]}
        cur.close()
        con.close()
        return h
    def GetCourse():
        course = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("Select * from masters.tbl_courses where is_active=1;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            course.append(h)
        cur2.close()
        con.close()
        return course
    def GetCenterBasedOnCourse(course_id):
        centers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC masters.sp_get_centers_based_on_course @course_id="+course_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            centers.append(h)
        cur2.close()
        con.close()
        return centers
    def GetTrainersBasedOnCenter(center_id):
        trainers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_trainer_based_on_center] @center_id="+center_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            trainers.append(h)
        cur2.close()
        con.close()
        return trainers
    def GetCenterManagerBasedOnCenter(center_id):
        centermanager = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_center_manager_based_on_center] @center_id="+center_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            centermanager.append(h)
        cur2.close()
        con.close()
        return centermanager

    def candidates_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_based_on_course] ?, ?,?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[11]
            fil=row[10]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    
    def add_edit_map_candidate_batch(candidate_ids,batch_id,course_id,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[add_edit_map_candidate_batch] ?, ?, ?, ?'
        values = (candidate_ids,batch_id,course_id,user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Mapping"}
        else:
            msg={"message":"Created Mapping"}
        return msg

    def qp_list(qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_qp_list] ?, ?, ?, ?, ?, ?'
        values = (qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[7]
            fil=row[6]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_qp_details(qp_name,qp_code,user_id,is_active,qp_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_qp ?, ?, ?, ?, ?'
        values = (qp_id,qp_name,qp_code,user_id,is_active)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","qp_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","qp_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Qualification Pack with the Qualification code already exists","qp_flag":2}
        return msg
    def get_qp_details(glob_qp_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_qp] where qp_id=?'
        values = (glob_qp_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h

    def candidate_list(candidate_id,course_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list] ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,course_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[7]
            fil=row[6]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def client_list(client_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_client_list] ?, ?, ?, ?, ?, ?'
        values = (client_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[7]
            fil=row[6]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_client_details(client_name,client_code,user_id,is_active,client_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_client] ?, ?, ?, ?, ?'
        values = (client_name,client_code,user_id,is_active,client_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","client_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","client_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Customer with the Customer code already exists","client_flag":2}
        return msg
    def get_client_detail(glob_client_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_client] where client_id=?'
        values = (glob_client_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h

    def region_list(region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_region_list] ?, ?, ?, ?, ?, ?'
        values = (region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[7]
            fil=row[6]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_region_details(region_name,region_code,user_id,is_active,region_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_region] ?, ?, ?, ?, ?'
        values = (region_name,region_code,user_id,is_active,region_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","region_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","region_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Region with the Region code already exists","region_flag":2}
        return msg
    def get_region_detail(glob_region_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_region] where region_id=?'
        values = (glob_region_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h
    

    
    def cluster_list(cluster_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_cluster_list] ?, ?, ?, ?, ?, ?'
        values = (cluster_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_cluster_details(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_cluster] ?, ?, ?, ?, ?, ?'
        values = (cluster_name,cluster_code,region_id,user_id,is_active,cluster_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","cluster_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","cluster_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Cluster with the Cluster code already exists","cluster_flag":2}
        return msg
    def get_cluster_detail(glob_cluster_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_cluster] where cluster_id=?'
        values = (glob_cluster_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    def get_all_Region():
        region = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_region] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            region.append(h)
        cur.close()
        con.close()
        return region

    def question_type_list(question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_question_type_list] ?, ?, ?, ?, ?, ?'
        values = (question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_question_type_details(question_type_name,user_id,is_active,question_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_question_type] ?, ?, ?, ?'
        values = (question_type_name,user_id,is_active,question_type_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_question_type_details(glob_question_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_question_type] where question_type_id=?'
        values = (glob_question_type_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h

    
    def section_type_list(section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_section_type_list] ?, ?, ?, ?, ?, ?'
        values = (section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_section_type_details(section_type_name,user_id,is_active,section_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_section_type] ?, ?, ?, ?'
        values = (section_type_name,user_id,is_active,section_type_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_section_type_details(glob_section_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section_type] where section_type_id=?'
        values = (glob_section_type_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h

    def section_list(section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_section_list] ?, ?, ?, ?, ?, ?'
        values = (section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_section_details(section_name,section_type_id,p_section,user_id,is_active,section_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_section] ?, ?, ?, ?, ?, ?'
        values = (section_name,section_type_id,p_section,user_id,is_active,section_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_section_details(glob_section_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section] where section_id=?'
        values = (glob_section_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    def all_section_types():
        sec_type=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section_type] where is_active=1'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sec_type.append(h)
        cur.close()
        con.close()
        return sec_type
    def all_parent_section():
        sec = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section] where is_active=1'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sec.append(h)
        cur.close()
        con.close()
        return sec
    
    # def state_and_district_list(state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
    #     content = {}
    #     d = []
    #     con = pyodbc.connect(conn_str)
    #     cur = con.cursor()
    #     sql = 'exec [content].[sp_get_section_list] ?, ?, ?, ?, ?, ?'
    #     values = (state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
    #     cur.execute(sql,(values))
    #     columns = [column[0].title() for column in cur.description]
    #     record="0"
    #     fil="0"
    #     for row in cur:
    #         record=row[8]
    #         fil=row[7]
    #         h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
    #         d.append(h)
    #     content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
    #     cur.close()
    #     con.close()
    #     return content

    
    def sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_sub_center_list] ?, ?, ?, ?, ?, ?, ?'
        values = (sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_sub_center_details(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_sub_center] ?, ?, ?, ?, ?, ?'
        values = (sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_sub_center_detail(glob_sub_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_sub_center] where sub_center_id=?'
        values = (glob_sub_center_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    
    def all_session_plan(course_id):
        sessionplans = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_session_plans] AS sp LEFT JOIN [content].[tbl_map_session_plan_course] AS map ON map.session_plan_id=sp.session_plan_id where map.course_id=?'
        values= course_id
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sessionplans.append(h)
        cur.close()
        con.close()
        return sessionplans
    def all_module(session_plan_id):
        modules = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_modules] where session_plan_id=?'
        values= session_plan_id
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            modules.append(h)
        cur.close()
        con.close()
        return modules
    def module_order_for_session_plan(session_plan_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT MAX(module_order) FROM [content].[tbl_modules] where session_plan_id=?'
        values= session_plan_id
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def get_session_order_for_module(module_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT MAX(session_order) FROM [content].[tbl_sessions] where module_id=?'
        values= module_id
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def sessioncode_for_module(module_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT code FROM [content].[tbl_modules] where module_id=?'
        values= module_id
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def module_session_list(session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_module_session_list] ?, ?, ?, ?, ?, ?, ?'
        values = (session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[9]
            fil=row[8]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7]}#,""+columns[12]+"":row[12],""+columns[14]+"":row[14]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_session_plan(session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_session_plan] ?, ?, ?, ?, ?, ?'
        values = (session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def add_module(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id):
        #print(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_module] ?, ?, ?, ?, ?, ?, ?'
        values = (module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def add_edit_session(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_session] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_session_detail(session_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_sessions] where session_id=?'
        values = (session_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[13]+"":row[13]}
        cur.close()
        con.close()
        return h
    ###########################################3  TMA BATCH



    @classmethod
    def get_trainer_data_db(cls):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
                                        SELECT	 trainer_name + ' (' + trainer_email + ')' AS trainer_name,
							 trainer_email
					FROM	 tma.tbl_trainers
					WHERE	 is_active=1
					ORDER BY trainer_name
        """
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    @classmethod
    def get_batch_list_count_db(cls, email_condition, batch_condition):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
WITH RES AS 
                        (
                            SELECT		DISTINCT 
                                        B.batch_id,
                                        B.trainer_name,
                                        B.trainer_email,
                                        B.batch_code,
                                        B.batch_start_date,
                                        B.batch_end_date,
                                        B.batch_status,
                                        B.batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        B.business_unit,
                                        B.center_name,
                                        B.center_type,
                                        CONCAT(B.course_code, '-', B.course_name) AS course_name,
                                        CONCAT(B.qp_code, '-', B.qp_name) AS qp_name,
                                        B.customer_name,
                                        CASE B.image_required WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
                                        (SELECT COUNT(S.session_id) FROM tma.tbl_sessions AS S WHERE S.course_id=B.course_id) AS session_count	
                            FROM		tma.tbl_batches AS B
                            WHERE		1=1 {}
                            AND			UPPER(batch_start_date) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(batch_end_date) NOT IN ('NULL','00-JAN-1900')
                            AND	 		UPPER(batch_active_status)='ACTIVE'
                            AND			UPPER(batch_status)='BATCH OPEN'
                        )
                      SELECT COUNT(batch_id) AS total_record_count 
                            FROM RES 
                            WHERE 1=1
                            {}   
                        
""".format(email_condition, batch_condition)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def getfilter_batch_list_count_db(cls, email_condition, batch_condition, search_condition):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """

WITH RES AS 
                        (
                            SELECT		DISTINCT 
                                        B.batch_id,
                                        B.trainer_name,
                                        B.trainer_email,
                                        B.batch_code,
                                        B.batch_start_date,
                                        B.batch_end_date,
                                        B.batch_status,
                                        B.batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        B.business_unit,
                                        B.center_name,
                                        B.center_type,
                                        CONCAT(B.course_code, '-', B.course_name) AS course_name,
                                        CONCAT(B.qp_code, '-', B.qp_name) AS qp_name,
                                        B.customer_name,
                                        CASE B.image_required WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
                                        (SELECT COUNT(S.session_id) FROM tma.tbl_sessions AS S WHERE S.course_id=B.course_id) AS session_count	
                            FROM		tma.tbl_batches AS B
                            WHERE		1=1 {}
                            AND			UPPER(batch_start_date) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(batch_end_date) NOT IN ('NULL','00-JAN-1900')
                            AND	 		UPPER(batch_active_status)='ACTIVE'
                            AND			UPPER(batch_status)='BATCH OPEN'
                        )
                      SELECT  COUNT(RES.batch_id) AS filtered_record_count 
                            FROM    RES
                            WHERE   1=1 
                            {}
                            {}
                            
                        
""".format(email_condition, batch_condition, search_condition)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def result_data_db(cls, email_condition, batch_condition, search_condition, order_by_statement, limit_statement):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
WITH RES AS 
                        (
                            SELECT		DISTINCT 
                                        B.batch_id,
                                        B.trainer_name,
                                        B.trainer_email,
                                        B.batch_code,
                                        B.batch_start_date,
                                        B.batch_end_date,
                                        B.batch_status,
                                        B.batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.batch_end_date) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.batch_start_date) AS DATE) AND CAST(UPPER(B.batch_end_date) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.batch_start_date) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        B.business_unit,
                                        B.center_name,
                                        B.center_type,
                                        CONCAT(B.course_code, '-', B.course_name) AS course_name,
                                        CONCAT(B.qp_code, '-', B.qp_name) AS qp_name,
                                        B.customer_name,
                                        CASE B.image_required WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
                                        (SELECT COUNT(S.session_id) FROM tma.tbl_sessions AS S WHERE S.course_id=B.course_id) AS session_count	
                            FROM		tma.tbl_batches AS B
                            WHERE		1=1 {}
                            AND			UPPER(batch_start_date) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(batch_end_date) NOT IN ('NULL','00-JAN-1900')
                            AND	 		UPPER(batch_active_status)='ACTIVE'
                            AND			UPPER(batch_status)='BATCH OPEN'
                        )
                        
                      SELECT
                             RES.trainer_name,
                             RES.trainer_email,
                             RES.batch_code,
                             RES.session_count,
                             RES.batch_start_date,
                             RES.batch_end_date,
                             RES.batch_status,
                             RES.batch_active_status,
                             RES.batch_stage_name,
                             RES.business_unit,
                             RES.center_name,
                             RES.center_type,
                             RES.course_name,
                             RES.qp_name,
                             RES.customer_name,
                             RES.image_required,
                             RES.batch_id
                             
                    FROM 	 RES 
                    WHERE    1=1
                    {}
                    {}
                    {}
                    {}
                        
""".format(email_condition, batch_condition, search_condition, order_by_statement, limit_statement)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    


    @classmethod
    def get_trainer_batch(cls,batch_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
SELECT		B.*,
                            T.trainer_name
                FROM		tma.tbl_batches AS B
                LEFT JOIN	tma.tbl_trainers AS T ON T.trainer_email=B.trainer_email
                WHERE		B.batch_id={}
""".format(batch_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def trainer_session_db(cls, trainer_email, batch_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """

                    SELECT		B.batch_id,
                                    S.session_id,
                                    S.session_name,
                                    FORMAT(STG1.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage1_log_time,
                                    STG1.image_file_name AS stage1_image,
                                    STG1.latitude AS stage1_latitide,
                                    STG1.longitude AS stage1_longitude,
                                    FORMAT(STG2.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage2_log_time,
                                    STG2.image_file_name AS stage2_image,
                                    STG2.latitude AS stage2_latitide,
                                    STG2.longitude AS stage2_longitude,
                                    FORMAT(STG3.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage3_log_time,
                                    STG3.image_file_name AS stage3_image,
                                    STG3.latitude AS stage3_latitide,
                                    STG3.longitude AS stage3_longitude,
                                    FORMAT(STG4.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage4_log_time,
                                    STG4.image_file_name AS stage4_image,
                                    STG4.latitude AS stage4_latitide,
                                    STG4.longitude AS stage4_longitude
                        FROM		tma.tbl_batches AS B

                        LEFT JOIN	tma.tbl_sessions AS S ON S.course_id=B.course_id 
                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG1 ON STG1.trainer_email='""" + trainer_email + """' AND STG1.batch_id=B.batch_id AND STG1.session_id=S.session_id AND STG1.stage_id=1
                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG2 ON STG2.trainer_email='""" + trainer_email + """' AND STG2.batch_id=B.batch_id AND STG2.session_id=S.session_id AND STG2.stage_id=2
                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG3 ON STG3.trainer_email='""" + trainer_email + """' AND STG3.batch_id=B.batch_id AND STG3.session_id=S.session_id AND STG3.stage_id=3
                        LEFT JOIN	tma.tbl_trainer_stage_log AS STG4 ON STG4.trainer_email='""" + trainer_email + """' AND STG4.batch_id=B.batch_id AND STG4.session_id=S.session_id AND STG4.stage_id=4
                        WHERE		B.batch_id={}
                        AND			ISNULL(S.session_id,0)>0
                        ORDER BY	S.session_id
""".format(batch_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    def get_candidate_attendance_db(batch_id, session_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
                WITH E AS
                    (
                        SELECT		CAST(A.[key] AS bigint) AS enrollment_id,
                                    REPLACE(CONVERT(VARCHAR,ATT.attendance_date,106),' ','-') AS attendance_date,
                                    A.[value] AS image_file_name
                        FROM		tma.tbl_candidate_attendance AS ATT
                        CROSS APPLY OPENJSON(ATT.attendance_json_data) AS A
                        WHERE		ATT.batch_id={}
                        AND			ATT.session_id={}
                    )
                    SELECT	C.candidate_name,
                                C.enrollment_id,
                                C.guardian_name,
                                C.phone,
                                C.gender,
                                C.date_of_birth,
                                E.attendance_date,
                                (CASE WHEN ISNULL(E.enrollment_id,0) > 0 THEN 'Present' ELSE 'NA' END) AS attendance,
                                E.image_file_name
                    FROM		tma.tbl_candidates AS C
                    INNER JOIN  tma.tbl_batches AS B ON UPPER(TRIM(B.batch_code))=UPPER(TRIM(C.batch_code))
                    LEFT JOIN	E ON E.enrollment_id=C.enrollment_id
                    WHERE		B.batch_id={}
                    AND			TRIM(ISNULL(C.candidate_name,''))<>''
                    AND			IIF(ISNULL(C.dropped_date,'')='','NULL',C.dropped_date)='NULL'
                    ORDER BY	C.candidate_name
                
                        """.format(batch_id, session_id, batch_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    @classmethod
    def get_candidate_group_attendance_db(cls,batch_id, session_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
                SELECT		A.[key] AS image_file_name,
                                A.[value] AS remarks
                    FROM		tma.tbl_candidate_attendance AS ATT
                    CROSS APPLY OPENJSON(ISNULL(NULLIF(ATT.group_attendance_image_json_data,''),'{}')) AS A
                    WHERE		ATT.batch_id={}
                    AND			ATT.session_id={}
                
                        """.format(batch_id, session_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data
