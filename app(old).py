from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify
from flask_session import Session
import pyodbc
import json
import os

app =Flask(__name__)
#MCLG_LIVE_Aug13
conn_str ="DRIVER={SQL SERVER};server=NEO-DEV-QA-01\SQLEXPRESS;database=MCLG_LIVE_Aug1;uid=sa;pwd=neo-dev-qa-01"
#conn_str ="DRIVER={SQL SERVER};server=DESKTOP-VN8J65K;database=MCLG_LIVE_Sep24;uid=sa;pwd=root"
"""
## Jagdish PC connect String
conn_str = (
            r'Driver={SQL Server};'
            r'Server=LNJAGDISH;'
            r'Database=MCLG_LIVE_Aug13;'
            r'Trusted_Connection=yes;'
            )
"""
displaymsg=""



app.secret_key = 'LN-NEO-Skills-Web'
#app.config["SESSION_PERMANENT"] = True
#sessions
@app.route('/log_out',methods=['GET', 'POST'])
def report_log_out():
    if g.user:
        session.pop('user_name', None)
        session.pop('user_id', None)
        return render_template("login.html",error=displaymsg)
    else:
        return render_template("login.html",error="Already logged out")
    ##return render_template('index.html')
    
@app.before_request
def before_request(): 
    g.user = None
    g.user_id = None
    g.user_role_id = None
    g.User_detail_with_ids = []
    if 'user_name' in session.keys():
        g.user = session['user_name']
        g.user_id = session['user_id']
        g.user_role = session['user_role_id']
        # print(g.user,g.user_id,g.user_role)
        g.User_detail_with_ids.append(g.user)
        g.User_detail_with_ids.append(g.user_id)
        g.User_detail_with_ids.append(g.user_role)
    
        
        # print(User_detail_with_ids)
    #return
####################################################################################################

#home_API's
@app.route("/")
def index():
    if g.user:        
        return render_template("home.html",values=g.user_id,html="")
    else:
        return render_template("login.html",error=displaymsg)\
        
@app.route("/EraseDisplayMsg")
def EraseDisplayMsg():
    global displaymsg
    displaymsg=""
    return redirect(url_for('index'))
    
@app.route("/home")
def home():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="")
    else:        
        return redirect(url_for('index'))

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['inemailaddress']
        passw = request.form['inpassword']
        
        #global tr
        global displaymsg
        tr =[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("SELECT u.user_id,u.user_name,u.user_role_id FROM users.tbl_users AS u LEFT JOIN users.tbl_user_details AS ud ON ud.user_id=u.user_id where ud.email='"+email+"' AND u.password='"+passw+"';")
        for row in cur:
            tr.append(row)
        cur.close()
        con.close()
        #return('1234   {}  1234'.format(tr))        
        if tr != []:
            session['user_name'] = tr[0][1]            
            session['user_id'] = tr[0][0]
            session['user_role_id'] = tr[0][2]            
            displaymsg=""
            #assign_sessions()
            return redirect(url_for('home'))
        else:
            displaymsg="wrong"
            return redirect(url_for('index'))

####################################################################################################

#project_API's
@app.route("/project_list_page")
def project_list_page():
    return render_template("project-list.html")

@app.route("/project_list" , methods=['GET','POST'])
def project_list():
        if request.method == 'POST':
            project_id = request.form['project_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            content = {}
            d = []
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [masters].[sp_get_project_list] ?, ?, ?, ?, ?, ?'
            values = (project_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
            #global count
            #count = count + 1
            return content

@app.route("/project")
def project():
    return render_template("home.html",values=g.user_id,html="project_list_page")

@app.route("/assign_project_add_edit_to_home", methods=['GET','POST'])
def assign_project_add_edit_to_home():    
    global glob_project_id
    print(request.form['hdn_project_id'])
    glob_project_id=request.form['hdn_project_id']
    return render_template("home.html",values=g.user_id,html="project_add_edit")

@app.route("/AllPracticeList")
def all_practice_list():
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
    practice_list={"Pratices":practice}
    return practice_list

@app.route("/AllClientList")
def all_client_list():
    client = []
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC [masters].[sp_get_all_clients] @client_id = NULL;")
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        client.append(h)
    cur2.close()
    con.close()
    client_list={"Clients":client}
    return client_list

@app.route("/add_project_details" , methods=['GET','POST'])
def add_project_details():
    project_name=request.form['ProjectName']
    client_id=request.form['ClientId']
    practice_id=request.form['PracticeId']
    user_id=tr[0][0]
    is_active='isactive' in request.form
    print(is_active)
    project_id=glob_project_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[masters].[sp_add_edit_project] ?, ?, ?, ?, ?, ?'
    values = (project_name,client_id,practice_id,user_id,is_active,project_id)
    cur.execute(sql,(values))
    cur.commit()
    cur.close()
    con.close()
    return render_template("home.html",values=g.user_id,html="project")

@app.route("/GetProjectDetails")
def get_project_details():
    global glob_project_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'SELECT * FROM [masters].[tbl_projects] where project_id=?'
    values = (glob_project_id)
    cur.execute(sql,(values))
    columns = [column[0].title() for column in cur.description]
    for row in cur:
        h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
    cur.close()
    con.close()
    indi_project={"ProjectDetail":h}
    print(indi_project)
    return indi_project

@app.route("/project_add_edit")
def project_add_edit():
    print(glob_project_id)
    return render_template("project-add-edit.html",project_id=glob_project_id)

####################################################################################################

#Client_API's
@app.route("/client_list_page")
def client_list_page():
    return render_template("client-list.html")

@app.route("/client_list" , methods=['GET','POST'])
def client_list():
    if request.method == 'POST':
            client_id = request.form['client_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            return content

@app.route("/client")
def client():
    return render_template("home.html",values=g.user_id,html="client_list_page")

@app.route("/client_add_edit")
def client_add_edit():
    return render_template("client-add-edit.html",client_id=glob_client_id)

@app.route("/assign_client_add_edit_to_home", methods=['GET','POST'])
def assign_client_add_edit_to_home():
    global glob_client_id
    print(request.form['hdn_client_id'])
    glob_client_id=request.form['hdn_client_id']
    return render_template("home.html",values=g.user_id,html="client_add_edit")

@app.route("/add_client_details" , methods=['GET','POST'])
def add_client_details():
    client_name=request.form['ClientName']
    client_code=request.form['ClientCode']
    user_id=tr[0][0]
    is_active='isactive' in request.form
    client_id=glob_client_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[masters].[sp_add_edit_client] ?, ?, ?, ?, ?'
    values = (client_name,client_code,user_id,is_active,client_id)
    cur.execute(sql,(values))
    cur.commit()
    cur.close()
    con.close()
    return render_template("home.html",values=g.user_id,html="client")

@app.route("/GetClientDetails")
def get_client_details():
    global glob_client_id
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
    indi_client={"ClientDetail":h}
    print(indi_client)
    return indi_client

####################################################################################################

#Practice_API's
@app.route("/practice_list_page")
def practice_list_page():
    return render_template("practice-list.html")

@app.route("/practice_list" , methods=['GET','POST'])
def practice_list():
    if request.method == 'POST':
            practice_id = request.form['practice_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            content = {}
            d = []
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [masters].[sp_get_practice_list] ?, ?, ?, ?, ?, ?'
            values = (practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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

@app.route("/practice")
def practice():
    return render_template("home.html",values=g.user_id,html="practice_list_page")

@app.route("/practice_add_edit")
def practice_add_edit():
    return render_template("practice-add-edit.html",practice_id=glob_practice_id)

@app.route("/assign_practice_add_edit_to_home", methods=['GET','POST'])
def assign_practice_add_edit_to_home():
    global glob_practice_id
    print(request.form['hdn_practice_id'])
    glob_practice_id=request.form['hdn_practice_id']
    return render_template("home.html",values=g.user_id,html="practice_add_edit")

@app.route("/add_practice_details" , methods=['GET','POST'])
def add_practice_details():
    practice_name=request.form['PracticeName']
    user_id=tr[0][0]
    is_active='isactive' in request.form
    practice_id=glob_practice_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[masters].[sp_add_edit_practices] ?, ?, ?, ?'
    values = (practice_name,user_id,is_active,practice_id)
    cur.execute(sql,(values))
    cur.commit()
    cur.close()
    con.close()
    return render_template("home.html",values=g.user_id,html="practice")

@app.route("/GetPracticeDetails")
def get_practice_details():
    global glob_practice_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'SELECT * FROM [masters].[tbl_practice] where practice_id=?'
    values = (glob_practice_id)
    cur.execute(sql,(values))
    columns = [column[0].title() for column in cur.description]
    for row in cur:
        h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
    cur.close()
    con.close()
    indi_practice={"PracticeDetail":h}
    print(indi_practice)
    return indi_practice

####################################################################################################

#Center_API's
@app.route("/center_list_page")
def center_list_page():
    if g.user:
        return render_template("Master/center-list.html")
    else:
        return redirect("/")

@app.route("/center_list" , methods=['GET','POST'])
def center_list():
    if request.method == 'POST':
            center_id = request.form['center_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            print(content)
            return content

@app.route("/center")
def center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")
    

@app.route("/center_add_edit")
def center_add_edit():
    if g.user:
        return render_template("Master/center-add-edit.html",center_id=glob_center_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_add_edit_to_home", methods=['GET','POST'])
def assign_center_add_edit_to_home():
    global glob_center_id
    print(request.form['hdn_center_id'])
    glob_center_id=request.form['hdn_center_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_center_details" , methods=['GET','POST'])
def add_center_details():
    center_name=request.form['CenterName']
    user_id=g.user_id
    is_active=request.form['isactive']
    center_id=glob_center_id
    center_type_id=request.form['CenterType']
    center_category_id=request.form['CenterCategory']
    country_id=request.form['CenterCountry']
    satet_id=request.form['CenterState']
    district_id=request.form['CenterDistrict']
    location_name=request.form['LocationName']
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_center")
def after_popup_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterDetails")
def get_center_details():
    global glob_center_id
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
    indi_center={"CenterDetail":h}
    print(indi_center)
    return indi_center

@app.route("/AllCenterTypes")
def all_center_type():
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
    center_t={"Center_Types":center_type}
    return center_t

@app.route("/AllCenterCategories")
def all_center_categories():
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
    center_categories={"Center_Categories":center_cat}
    return center_categories

@app.route("/AllCountries")
def all_countries():
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
    countries_for={"Countries":countries}
    return countries_for

@app.route("/AllStatesBasedOnCountry", methods=['GET','POST'])
def all_states_based_on_country():
    states = []
    country_id=request.form['country_id']
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC	[masters].[sp_get_all_states_based_on_country] @country_id = "+country_id)
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        states.append(h)
    cur2.close()
    con.close()
    states_for_country={"States":states}
    return states_for_country

@app.route("/AllDistrictsBasedOnState", methods=['GET','POST'])
def all_districts_based_on_state():
    districts = []
    state_id=request.form['state_id']
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC	[masters].[sp_get_all_districts_based_on_state] @state_id = "+state_id)
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        districts.append(h)
    cur2.close()
    con.close()
    districts_for_state={"Districts":districts}
    return districts_for_state


####################################################################################################

#User_role_API's
@app.route("/user_role_list_page")
def user_role_list_page():
    if g.user:
        return render_template("User_Management/user-role-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user_role_list" , methods=['GET','POST'])
def user_role_list():
    if request.method == 'POST':
            user_role_id = request.form['user_role_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            return content

@app.route("/user_role")
def user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user_role_add_edit")
def user_role_add_edit():
    if g.user:
        return render_template("User_Management/user-role-add-edit.html",user_role_id=glob_user_role_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_user_role_add_edit_to_home", methods=['GET','POST'])
def assign_user_role_add_edit_to_home():
    global glob_user_role_id
    print(request.form['hdn_user_role_id'])
    glob_user_role_id=request.form['hdn_user_role_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_user_role_details" , methods=['GET','POST'])
def add_user_role_details():
    user_role_name=request.form['UserRoleName']
    user_id=g.user_id
    is_active=request.form['isactive']
    user_role_id=glob_user_role_id
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_user_role")
def after_popup_user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetUserRoleDetails")
def get_user_role_details():
    global glob_user_role_id
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
    indi_user_role={"UserRoleDetail":h}
    print(indi_user_role)
    return indi_user_role

####################################################################################################

#Section_type_API's
@app.route("/section_type_list_page")
def section_type_list_page():
    return render_template("section-type-list.html")

@app.route("/section_type_list" , methods=['GET','POST'])
def section_type_list():
    if request.method == 'POST':
            section_type_id = request.form['section_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            return content

@app.route("/section_type")
def section_type():
    return render_template("home.html",values=g.user_id,html="section_type_list_page")

@app.route("/section_type_add_edit")
def section_type_add_edit():
    return render_template("section-type-add-edit.html",section_type_id=glob_section_type_id)

@app.route("/assign_section_type_add_edit_to_home", methods=['GET','POST'])
def assign_section_type_add_edit_to_home():
    global glob_section_type_id
    print(request.form['hdn_section_type_id'])
    glob_section_type_id=request.form['hdn_section_type_id']
    return render_template("home.html",values=g.user_id,html="section_type_add_edit")

@app.route("/add_section_type_details" , methods=['GET','POST'])
def add_section_type_details():
    section_type_name=request.form['SectionTypeName']
    user_id=tr[0][0]
    is_active='isactive' in request.form
    section_type_id=glob_section_type_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[content].[sp_add_edit_section_type] ?, ?, ?, ?'
    values = (section_type_name,user_id,is_active,section_type_id)
    cur.execute(sql,(values))
    cur.commit()
    cur.close()
    con.close()
    return render_template("home.html",values=g.user_id,html="section_type")

@app.route("/GetSectionTypeDetails")
def get_section_type_details():
    global glob_section_type_id
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
    indi_section_type={"SectionTypeDetail":h}
    print(indi_section_type)
    return indi_section_type

####################################################################################################

#QuestionType_API's
@app.route("/question_type_list_page")
def question_type_list_page():
    return render_template("question-type-list.html")

@app.route("/question_type_list" , methods=['GET','POST'])
def question_type_list():
    if request.method == 'POST':
            question_type_id = request.form['question_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            return content

@app.route("/question_type")
def question_type():
    return render_template("home.html",values=g.user_id,html="question_type_list_page")

@app.route("/question_type_add_edit")
def question_type_add_edit():
    return render_template("question-type-add-edit.html",question_type_id=glob_question_type_id)

@app.route("/assign_question_type_add_edit_to_home", methods=['GET','POST'])
def assign_question_type_add_edit_to_home():
    global glob_question_type_id
    print(request.form['hdn_question_type_id'])
    glob_question_type_id=request.form['hdn_question_type_id']
    return render_template("home.html",values=g.user_id,html="question_type_add_edit")

@app.route("/add_question_type_details" , methods=['GET','POST'])
def add_question_type_details():
    question_type_name=request.form['QuestionTypeName']
    user_id=tr[0][0]
    is_active='isactive' in request.form
    question_type_id=glob_question_type_id
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[content].[sp_add_edit_question_type] ?, ?, ?, ?'
    values = (question_type_name,user_id,is_active,question_type_id)
    cur.execute(sql,(values))
    cur.commit()
    cur.close()
    con.close()
    return render_template("home.html",values=g.user_id,html="question_type")

@app.route("/GetQuestionTypeDetails")
def get_question_type_details():
    global glob_question_type_id
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
    indi_question_type={"QuestionTypeDetail":h}
    print(indi_question_type)
    return indi_question_type

####################################################################################################

#Course_API's
@app.route("/course_list_page")
def course_list_page():
    if g.user:
        return render_template("Content/course-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/course")
def course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/course_list" , methods=['GET','POST'])
def course_list():
    if request.method == 'POST':
            course_id = request.form['course_id'] 
            practice_id = request.form['practice_id']
            project_id = request.form['project_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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

@app.route("/AllProjectsBasedOnPractice", methods=['GET','POST'])
def all_projects_based_on_practice():
    projects = []
    practice_id = request.form['practice_id']
    project_id = request.form['project_id']
    print(practice_id)
    print(project_id)
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
    project_list={"Projects":projects}
    return project_list

@app.route("/AllCenterList")
def all_center_list():
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
    center_list={"Centers":center}
    return center_list

@app.route("/course_add_edit")
def course_add_edit():
    if g.user:
        return render_template("Content/course-add-edit.html",course_id=glob_course_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_course_add_edit_to_home", methods=['GET','POST'])
def assign_course_type_add_edit_to_home():
    global glob_course_id
    print(request.form['hdn_course_id'])
    glob_course_id=request.form['hdn_course_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_course_details" , methods=['GET','POST'])
def add_course_details():
    center_ids=""
    course_name=request.form['CourseName']
    project_id=13
    user_id=g.user_id
    is_active=request.form['isactive']
    center_ids=request.form['CenterId']
    items=request.form['SessionJSON']
    # headers = ("session_name", "session_duration")
    # jsvalues = (
    #     request.form.getlist('session_name'),
    #     request.form.getlist('session_duration')        
    # )
    # items = [{} for i in range(len(jsvalues[0]))]
    # for x,i in enumerate(jsvalues):
    #     for _x,_i in enumerate(i):
    #         items[_x][headers[x]] = _i
    # print(project_id)
    # for i in center_idlist:
    #     print(i)
    #     if center_ids == "":
    #         center_ids = i
    #     else:
    #         center_ids = center_ids + "," + i
    #print(center_ids)
    course_id=glob_course_id
    old="'"
    new='"'
    print(items,course_name,project_id,user_id,is_active,center_ids,course_id)
    con = pyodbc.connect(conn_str)
    cur = con.cursor()
    sql = 'exec	[content].[sp_add_edit_course] ?, ?, ?, ?, ?, ?, ?'
    if items == "[]":
        values = (course_name,project_id,user_id,is_active,center_ids,course_id,'')
    else:
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_course")
def after_popup_course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCourseDetails")
def get_course_details():
    global glob_course_id
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
    indi_course={"CourseDetail":h}
    print(indi_course)
    return indi_course

####################################################################################################

#Users_API's
@app.route("/user_list_page")
def user_list_page():
    if g.user:
        return render_template("User_Management/user-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user")
def user():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user_list" , methods=['GET','POST'])
def user_list():
    if request.method == 'POST':
            user_id = request.form['user_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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

@app.route("/user_add_edit")
def user_add_edit():
    if g.user:
        print(glob_user_id)
        return render_template("User_Management/user-add-edit.html",user_id=glob_user_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_user_add_edit_to_home", methods=['GET','POST'])
def assign_user_type_add_edit_to_home():
    global glob_user_id
    print(request.form['hdn_user_id'])
    glob_user_id=request.form['hdn_user_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_user_details" , methods=['GET','POST'])
def add_user_details():
    try:
        global glob_user_id
        center_ids=""
        user_role_id=request.form['UserRole']
        first_name=request.form['FirstName']
        last_name=request.form['LastName']
        email=request.form['Email']
        mobile=request.form['MobileNumber']
        created_id=g.user_id
        is_active=request.form['isactive']
        user_id=glob_user_id
        center_ids=request.form['CenterId']
        is_reporting_manager=request.form['IsReportingManager']
        print(center_ids)
        # print(center_idlist)
        # for i in center_idlist:
        #     print(i)
        #     if center_ids == "":
        #         center_ids = i
        #     else:
        #         center_ids = center_ids + "," + i
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
        
        print(msg)
        popupMessage = {"PopupMessage": msg}
        return popupMessage
    except Exception as e:
        msg={"message":str(e), "UserId": 0}
        return {"PopupMessage": msg}

@app.route("/after_popup_user")
def after_popup_user():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/AllUserRole")
def all_user_role():
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
    userrole_list={"UserRoles":userrole}
    return userrole_list

@app.route("/GetUserDetails")
def get_user_details():
    global glob_user_id
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
    indi_user={"UserDetail":h}
    print(indi_user)
    return indi_user

####################################################################################################

#Center_Type_API's
@app.route("/center_type_list_page")
def center_type_list_page():
    if g.user:
        return render_template("Master/center-type-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_type_list" , methods=['GET','POST'])
def center_type_list():
    if request.method == 'POST':
            center_type_id = request.form['center_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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

@app.route("/center_type")
def center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_type_add_edit")
def center_type_add_edit():
    if g.user:
        return render_template("Master/center-type-add-edit.html",center_type_id=glob_center_type_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_type_add_edit_to_home", methods=['GET','POST'])
def assign_center_type_add_edit_to_home():
    global glob_center_type_id
    print(request.form['hdn_center_type_id'])
    glob_center_type_id=request.form['hdn_center_type_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_center_type_details" , methods=['GET','POST'])
def add_center_type_details():
    center_type_name=request.form['CenterTypeName']
    user_id=g.user_id
    is_active=request.form['isactive']
    center_type_id=glob_center_type_id
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_center_type")
def after_popup_center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterTypeDetails")
def get_center_type_details():
    global glob_center_type_id
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
    indi_center_type={"CenterTypeDetail":h}
    print(indi_center_type)
    return indi_center_type


####################################################################################################

#Center_Category_API's
@app.route("/center_category_list_page")
def center_category_list_page():
    if g.user:
        return render_template("Master/center-category-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_category_list" , methods=['GET','POST'])
def center_category_list():
    if request.method == 'POST':
            center_category_id = request.form['center_category_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
            #global count
            #count = count + 1
            return content

@app.route("/center_category")
def center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_category_add_edit")
def center_category_add_edit():
    if g.user:
        return render_template("Master/center-category-add-edit.html",center_category_id=glob_center_category_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_category_add_edit_to_home", methods=['GET','POST'])
def assign_center_category_add_edit_to_home():
    global glob_center_category_id
    print(request.form['hdn_center_category_id'])
    glob_center_category_id=request.form['hdn_center_category_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_center_category_details" , methods=['GET','POST'])
def add_center_category_details():
    center_category_name=request.form['CenterCategoryName']
    user_id=g.user_id
    is_active=request.form['isactive']
    center_category_id=glob_center_category_id
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_center_category")
def after_popup_center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterCategoryDetails")
def get_center_category_details():
    global glob_center_category_id
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
    indi_center_category={"CenterCategoryDetail":h}
    print(indi_center_category)
    return indi_center_category

####################################################################################################

#Batch_API's

@app.route("/batch_list_page")
def batch_list_page():
    if g.user:
        return render_template("Batch/batch-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_list" , methods=['GET','POST'])
def batch_list():
    if request.method == 'POST':
            batch_id = request.form['batch_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
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
                record=row[16]
                fil=row[15]
                h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14]}
                d.append(h)
            content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
            cur.close()
            con.close()
            #global count
            #count = count + 1
            print(content)
            return content

@app.route("/batch")
def batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_add_edit")
def batch_add_edit():
    if g.user:
        return render_template("Batch/batch-add-edit.html",batch_id=glob_batch_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_batch_add_edit_to_home", methods=['GET','POST'])
def assign_batch_add_edit_to_home():
    global glob_batch_id
    print(request.form['hdn_batch_id'])
    glob_batch_id=request.form['hdn_batch_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/add_batch_details" , methods=['GET','POST'])
def add_batch_details():
    batch_id=glob_batch_id
    batch_name=request.form['BatchName']
    course_id=request.form['CourseId']
    center_id=request.form['CenterId']
    trainer_id=request.form['TrainerId']
    center_manager_id=request.form['CentralManagerId']
    start_date=request.form['StartDate']
    end_date=request.form['EndDate']
    start_time=request.form['StartTime']
    end_time=request.form['EndTime']
    user_id=g.user_id
    is_active=request.form['isactive']
    print (batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time)
    # return end_time
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
    print(msg)
    popupMessage = {"PopupMessage": msg}
    return popupMessage

@app.route("/after_popup_batch")
def after_popup_batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetBatchDetails")
def get_batch_details():
    global glob_batch_id
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
    indi_batch={"BatchDetail":h}
    print(indi_batch)
    return indi_batch

@app.route("/AllCourseList")
def all_course_list():
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
    course_f={"Courses":course}
    return course_f

@app.route("/CentersBasedOnCourse", methods=['GET','POST'])
def centers_based_on_course():
    centers = []
    course_id=request.form['course_id']
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC masters.sp_get_centers_based_on_course @course_id="+course_id)
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        centers.append(h)
    cur2.close()
    con.close()
    centers_f={"Centers":centers}
    return centers_f

@app.route("/TrainersBasedOnCenter", methods=['GET','POST'])
def trainers_based_on_center():
    trainers = []
    center_id=request.form['center_id']
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC [masters].[sp_get_trainer_based_on_center] @center_id="+center_id)
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        trainers.append(h)
    cur2.close()
    con.close()
    trainers_f={"Trainers":trainers}
    return trainers_f

@app.route("/CenterManagerBasedOnCenter", methods=['GET','POST'])
def center_manager_based_on_center():
    centermanager = []
    center_id=request.form['center_id']
    print(center_id)
    con = pyodbc.connect(conn_str)
    cur2 = con.cursor()
    cur2.execute("EXEC [masters].[sp_get_center_manager_based_on_center] @center_id="+center_id)
    columns = [column[0].title() for column in cur2.description]
    for r in cur2:
        h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
        centermanager.append(h)
    cur2.close()
    con.close()
    print(centermanager)
    centermanager_f={"CenterManager":centermanager}
    return centermanager_f

if __name__ == "__main__":
    app.run(debug=True)
    
