import pyodbc
from .config import *
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
        values = (11)
        
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
            record=row[17]
            fil=row[16]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_center_details(center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_centers] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name)
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
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10]}
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
    def add_course_details(course_name,project_id,user_id,is_active,center_ids,course_id,items):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_course] ?, ?, ?, ?, ?, ?, ?'
        values = (course_name,project_id,user_id,is_active,center_ids,course_id,items)
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
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h
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
                    msg={"message":"User with the email id already exists", "UserId": UserId}
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
            record=row[17]
            fil=row[16]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_batch_details(batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	batches.sp_add_edit_batches ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active)
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
    def get_batch_details(glob_batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [batches].[tbl_batches] where batch_id=?'
        values = (glob_batch_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[12]+"":row[12]}
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
