from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify
from flask_restful import Resource
from flask_restful import Api
#from flask_session import Session
from Models import Content
from Models import Master
from Models import UsersM
from Models import Batch
from Database import config
from Database import Database
import course_api
import center_category_api
import center_api

app = Flask(__name__)

api = Api(app)

app.config["SESSION_PERMANENT"] = True

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
    g.course_id = None
    g.center_category_id = None
    g.center_type_id = None
    g.center_id = None
    g.user_id = None
    g.user_role_id = None
    g.web_user_id = None
    g.batch_id = None
    
    g.User_detail_with_ids = []
    if 'user_name' in session.keys():
        g.user = session['user_name']
        g.user_id = session['user_id']
        g.user_role = session['user_role_id']
        # print(g.user,g.user_id,g.user_role)
        g.User_detail_with_ids.append(g.user)
        g.User_detail_with_ids.append(g.user_id)
        g.User_detail_with_ids.append(g.user_role)
    if 'course_id' in session.keys():
        g.course_id = session['course_id']
    if 'center_category_id' in session.keys():
        g.center_category_id = session['center_category_id']
    if 'center_type_id' in session.keys():
        g.center_type_id = session['center_type_id']
    if 'center_id' in session.keys():
        g.center_id = session['center_id']
    if 'web_user_role_id' in session.keys():
        g.user_role_id = session['web_user_role_id']
    if 'web_user_id' in session.keys():
        g.web_user_id = session['web_user_id']
    if 'batch_id' in session.keys():
        g.batch_id = session['batch_id']
    


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

@app.route("/center")
def center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")
    

@app.route("/center_add_edit")
def center_add_edit():
    if g.user:
        return render_template("Master/center-add-edit.html",center_id=g.center_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_add_edit_to_home", methods=['GET','POST'])
def assign_center_add_edit_to_home():
    #global glob_center_id
    #print(request.form['hdn_center_id'])
    #glob_center_id=request.form['hdn_center_id']
    session['center_id'] = request.form['hdn_center_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_center")
def after_popup_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center")
    else:
        return render_template("login.html",error="Session Time Out!!")


class add_center_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_name=request.form['CenterName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_id=request.form['CenterId']
            center_type_id=request.form['CenterType']
            center_category_id=request.form['CenterCategory']
            country_id=request.form['CenterCountry']
            satet_id=request.form['CenterState']
            district_id=request.form['CenterDistrict']
            location_name=request.form['LocationName']
            return Master.add_center(center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name)

class get_center_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return jsonify(Master.AllCenters(g.center_id))
            

api.add_resource(center_api.center_list, '/center_list')
api.add_resource(center_api.all_center_type, '/AllCenterTypes')
api.add_resource(center_api.all_center_categories, '/AllCenterCategories')
api.add_resource(center_api.all_countries, '/AllCountries')
api.add_resource(center_api.all_states_based_on_country, '/AllStatesBasedOnCountry')
api.add_resource(center_api.all_districts_based_on_state, '/AllDistrictsBasedOnState')

api.add_resource(get_center_details, '/GetCenterDetails')
api.add_resource(add_center_details, '/add_center_details')
####################################################################################################
#Center_Type_API's
@app.route("/center_type_list_page")
def center_type_list_page():
    if g.user:
        return render_template("Master/center-type-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/center_type")
def center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_type_add_edit")
def center_type_add_edit():
    if g.user:
        return render_template("Master/center-type-add-edit.html",center_type_id=g.center_type_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_type_add_edit_to_home", methods=['GET','POST'])
def assign_center_type_add_edit_to_home():
    #global glob_center_type_id
    #print(request.form['hdn_center_type_id'])
    #glob_center_type_id=request.form['hdn_center_type_id']
    #return request.form['hdn_center_type_id']
    session['center_type_id'] = request.form['hdn_center_type_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_center_type")
def after_popup_center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

class add_center_type_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_type_name=request.form['CenterTypeName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_type_id=request.form['CenterTypeId']
            return Master.add_center_type(center_type_name,user_id,is_active,center_type_id)



class get_center_type_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            try:
                #global glob_center_type_id ||| 
                return jsonify(Master.get_center_type(g.center_type_id))
            except Exception as e:
                return {'message':str(e)}
                
class center_type_list(Resource):
    @staticmethod
    def post():
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



api.add_resource(center_type_list, '/center_type_list')
api.add_resource(add_center_type_details, '/add_center_type_details')
api.add_resource(get_center_type_details, '/GetCenterTypeDetails')
 
####################################################################################################
#Center_Category_API's
@app.route("/center_category_list_page")
def center_category_list_page():
    if g.user:
        return render_template("Master/center-category-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")
   
@app.route("/center_category")
def center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_category_add_edit")
def center_category_add_edit():
    if g.user:
        return render_template("Master/center-category-add-edit.html",center_category_id=g.center_category_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_category_add_edit_to_home", methods=['GET','POST'])
def assign_center_category_add_edit_to_home():
    #global glob_center_category_id
    #print(request.form['hdn_center_category_id'])
    #glob_center_category_id=request.form['hdn_center_category_id']
    session['center_category_id'] = request.form['hdn_center_category_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

    
@app.route("/after_popup_center_category")
def after_popup_center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category")
    else:
        return render_template("login.html",error="Session Time Out!!")

class add_center_category_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_category_name=request.form['CenterCategoryName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_category_id=request.form['CenterCategoryId']
            return Master.add_center_category(center_category_name,user_id,is_active,center_category_id)


class get_center_category_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            #global glob_center_category_id
            #g.center_category_id
            return jsonify(Master.get_center_category(g.center_category_id))


api.add_resource(center_category_api.center_category_list, '/center_category_list')
api.add_resource(add_center_category_details, '/add_center_category_details')
api.add_resource(get_center_category_details, '/GetCenterCategoryDetails')
 
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

@app.route("/course_add_edit")
def course_add_edit():
    if g.user:
        return render_template("Content/course-add-edit.html",course_id=g.course_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_course_add_edit_to_home", methods=['GET','POST'])
def assign_course_type_add_edit_to_home():
    
    #global glob_course_id
    #return(request.form['hdn_course_id'])
    #glob_course_id= request.form['hdn_course_id']
    session['course_id'] = request.form['hdn_course_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_course")
def after_popup_course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course")
    else:
        return render_template("login.html",error="Session Time Out!!")

######### API with g data
class add_course_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_name=request.form['CourseName']
            project_id=13    ### WHY project id is fixed
            user_id=g.user_id
            is_active=request.form['isactive']
            center_ids=request.form['CenterId']
            items=request.form['SessionJSON']
            course_id=request.form['CourseId']
            return Content.add_course(course_name,project_id,user_id,is_active,center_ids,course_id,items)
            
class GetCourseDetails(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            #global glob_course_id
            #return glob_course_id
            return Content.get_course(g.course_id)


api.add_resource(course_api.course_list, '/course_list')
api.add_resource(course_api.AllCenterList, '/AllCenterList')
api.add_resource(course_api.AllPracticeList, '/AllPracticeList')
api.add_resource(course_api.AllProjectsBasedOnPractice, '/AllProjectsBasedOnPractice')

api.add_resource(add_course_details, '/add_course_details')
api.add_resource(GetCourseDetails, '/GetCourseDetails')   

####################################################################################################

#User_role_API's
@app.route("/user_role_list_page")
def user_role_list_page():
    if g.user:
        return render_template("User_Management/user-role-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/user_role")
def user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/user_role_add_edit")
def user_role_add_edit():
    if g.user:
        return render_template("User_Management/user-role-add-edit.html",user_role_id=g.user_role_id)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/assign_user_role_add_edit_to_home", methods=['GET','POST'])
def assign_user_role_add_edit_to_home():
    session['web_user_role_id'] = request.form['hdn_user_role_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_user_role")
def after_popup_user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role")
    else:
        return render_template("login.html",error="Session Time Out!!")

##############################  API   #########################
class user_role_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_role_id = request.form['user_role_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return UsersM.user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)


class add_user_role_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_role_name=request.form['UserRoleName']
            user_id=g.user_id
            is_active=request.form['isactive']
            user_role_id=g.user_role_id
            return UsersM.add_user_role(user_role_name,user_id,is_active,user_role_id)
                    
class get_user_role_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return UsersM.get_user_role(g.user_role_id)



api.add_resource(get_user_role_details, '/GetUserRoleDetails')
api.add_resource(add_user_role_details, '/add_user_role_details')
api.add_resource(user_role_list, '/user_role_list')

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

@app.route("/user_add_edit")
def user_add_edit():
    if g.user:
        print(glob_user_id)
        return render_template("User_Management/user-add-edit.html",user_id=g.web_user_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_user_add_edit_to_home", methods=['GET','POST'])
def assign_user_type_add_edit_to_home():
    session['web_user_id']=request.form['hdn_user_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_user")
def after_popup_user():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user")
    else:
        return render_template("login.html",error="Session Time Out!!")

####################  API  #######################
class user_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id = request.form['user_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return UsersM.user_list(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)



class add_user_details(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                center_ids=""
                user_role_id=request.form['UserRole']
                first_name=request.form['FirstName']
                last_name=request.form['LastName']
                email=request.form['Email']
                mobile=request.form['MobileNumber']
                created_id=g.user_id
                is_active=request.form['isactive']
                user_id=g.web_user_id
                center_ids=request.form['CenterId']
                is_reporting_manager=request.form['IsReportingManager']
                return UsersM.add_user(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager)
        except Exception as e:
            msg={"message":str(e), "UserId": 0}
            return {"PopupMessage": msg}
                    
class all_user_role(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return UsersM.AllUserRole()


class get_user_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return UsersM.get_user(g.web_user_id)



api.add_resource(user_list, '/user_list')
api.add_resource(add_user_details, '/add_user_details')
api.add_resource(all_user_role, '/AllUserRole')
api.add_resource(get_user_details, '/GetUserDetails')

####################################################################################################
#Batch_API's

@app.route("/batch_list_page")
def batch_list_page():
    if g.user:
        return render_template("Batch/batch-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/batch")
def batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_add_edit")
def batch_add_edit():
    if g.user:
        return render_template("Batch/batch-add-edit.html",batch_id=g.batch_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_batch_add_edit_to_home", methods=['GET','POST'])
def assign_batch_add_edit_to_home():
    
    session['batch_id']=request.form['hdn_batch_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_batch")
def after_popup_batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch")
    else:
        return render_template("login.html",error="Session Time Out!!")
    
#################################  API  ###################

class add_batch_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            batch_id=g.batch_id
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



class batch_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            batch_id = request.form['batch_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Batch.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

 

class get_batch_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Batch.get_batch(g.batch_id)



class all_course_list(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Batch.AllCourse()



class centers_based_on_course(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_id=request.form['course_id']
            return Batch.AllCenterOnCourse(course_id)

class trainers_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id=request.form['center_id']
            return Batch.AllTrainersOnCenter(center_id)


class center_manager_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id=request.form['center_id']
            return Batch.AllCenterManagerOnCenter(center_id)

api.add_resource(add_batch_details, '/add_batch_details')
api.add_resource(batch_list, '/batch_list')
api.add_resource(get_batch_details, '/GetBatchDetails')
api.add_resource(all_course_list, '/AllCourseList')
api.add_resource(centers_based_on_course, '/CentersBasedOnCourse')
api.add_resource(trainers_based_on_center, '/TrainersBasedOnCenter')
api.add_resource(center_manager_based_on_center, '/CenterManagerBasedOnCenter')




if __name__ == '__main__':
    #session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.run()
