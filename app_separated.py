from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify
#from flask_session import Session
from Models import Content
from Models import Master
from Models import UsersM
from Models import Batch
from Database import config
from Database import Database

app = Flask(__name__)

app.secret_key = config.secret_key

#sessions
@app.route('/log_out',methods=['GET', 'POST'])
def report_log_out():
    if g.user:
        session.pop('user_name', None)
        session.pop('user_id', None)
        return render_template("login.html",error=config.displaymsg)
    else:
        return render_template("login.html",error="Already logged out")
    
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

#home_API's
@app.route("/")
def index():
    if g.user:        
        return render_template("home.html",values=g.user_id,html="")
    else:
        return render_template("login.html",error=config.displaymsg)
        
@app.route("/EraseDisplayMsg")
def EraseDisplayMsg():
    config.displaymsg=""
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
        tr = []
        email = request.form['inemailaddress']
        passw = request.form['inpassword']
        tr = Database.Login(email,passw)
        if tr != []:
            session['user_name'] = tr[0][1]            
            session['user_id'] = tr[0][0]
            session['user_role_id'] = tr[0][2]            
            config.displaymsg=""
            return redirect(url_for('home'))
            #assign_sessions()
            
        else:
            config.displaymsg="wrong"
            return redirect(url_for('index'))
        
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
            Center_lt = Master.center_list(center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return Center_lt

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
    return Master.add_center(center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name)

@app.route("/after_popup_center")
def after_popup_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterDetails")
def get_center_details():
    global glob_center_id
    return Master.AllCenters(glob_center_id)

@app.route("/AllCenterTypes")
def all_center_type():
    return Master.AllCenterTypes()

@app.route("/AllCenterCategories")
def all_center_categories():
    return Master.AllCenterCategory()

@app.route("/AllCountries")
def all_countries():
    return Master.AllCountry()

@app.route("/AllStatesBasedOnCountry", methods=['GET','POST'])
def all_states_based_on_country():
    country_id=request.form['country_id']
    return Master.AllStatesOnCountry(country_id)

@app.route("/AllDistrictsBasedOnState", methods=['GET','POST'])
def all_districts_based_on_state():
    state_id=request.form['state_id']
    return Master.AllDistrictsOnState(state_id)


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
            CenterT = Master.center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return CenterT

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
    return Master.add_center_type(center_type_name,user_id,is_active,center_type_id)

@app.route("/after_popup_center_type")
def after_popup_center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterTypeDetails")
def get_center_type_details():
    global glob_center_type_id
    return Master.get_center_type(glob_center_type_id)

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
            return Master.center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

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
    return Master.add_center_category(center_category_name,user_id,is_active,center_category_id)

@app.route("/after_popup_center_category")
def after_popup_center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCenterCategoryDetails")
def get_center_category_details():
    global glob_center_category_id
    return Master.get_center_category(glob_center_category_id)

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
            return Content.course_list(course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

@app.route("/AllPracticeList")
def all_practice_list():
    return Content.AllPractice()

@app.route("/AllProjectsBasedOnPractice", methods=['GET','POST'])
def all_projects_based_on_practice():
    practice_id = request.form['practice_id']
    project_id = request.form['project_id']
    return Content.AllProjectOnPractice(project_id,practice_id)

@app.route("/AllCenterList")
def all_center_list():
    return Content.AllCenter()

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
    course_name=request.form['CourseName']
    project_id=13
    user_id=g.user_id
    is_active=request.form['isactive']
    center_ids=request.form['CenterId']
    items=request.form['SessionJSON']
    course_id=glob_course_id
    return Content.add_course(course_name,project_id,user_id,is_active,center_ids,course_id,items)
    

@app.route("/after_popup_course")
def after_popup_course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetCourseDetails")
def get_course_details():
    global glob_course_id
    return Content.get_course(glob_course_id)

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
            return UsersM.user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

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
    return UsersM.add_user_role(user_role_name,user_id,is_active,user_role_id)

@app.route("/after_popup_user_role")
def after_popup_user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetUserRoleDetails")
def get_user_role_details():
    global glob_user_role_id
    return UsersM.get_user_role(glob_user_role_id)

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
            return UsersM.user_list(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

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
        # print(center_ids)
        return UsersM.add_user(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager)
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
    return UsersM.AllUserRole()

@app.route("/GetUserDetails")
def get_user_details():
    global glob_user_id
    return UsersM.get_user(glob_user_id)

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
            return Batch.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

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
    return Batch.add_batch(batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active)

@app.route("/after_popup_batch")
def after_popup_batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/GetBatchDetails")
def get_batch_details():
    global glob_batch_id
    return Batch.get_batch(glob_batch_id)

@app.route("/AllCourseList")
def all_course_list():
    return Batch.AllCourse()

@app.route("/CentersBasedOnCourse", methods=['GET','POST'])
def centers_based_on_course():
    course_id=request.form['course_id']
    return Batch.AllCenterOnCourse(course_id)

@app.route("/TrainersBasedOnCenter", methods=['GET','POST'])
def trainers_based_on_center():
    center_id=request.form['center_id']
    return Batch.AllTrainersOnCenter(center_id)

@app.route("/CenterManagerBasedOnCenter", methods=['GET','POST'])
def center_manager_based_on_center():
    center_id=request.form['center_id']
    return Batch.AllCenterManagerOnCenter(center_id)

if __name__ == '__main__':
    app.run(debug=True)
