from Database import Database
class Content:
    def course_list(course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        course_l = Database.course_list(course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return course_l
    def AllPractice():
        practice_list={"Pratices":Database.GetPractice()}
        return practice_list
    def AllProjectOnPractice(project_id,practice_id):
        project_list={"Projects":Database.GetProjectBasedOnPractice(project_id,practice_id)}
        return project_list
    def AllCenter():
        center_list={"Centers":Database.GetAllCenter()}
        return center_list
    def add_course(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items):
        if items == "[]":
            popupMessage = {"PopupMessage": Database.add_course_details(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,'')}
            return popupMessage
        else:
            popupMessage = {"PopupMessage": Database.add_course_details(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items)}
            return popupMessage
    def get_course(glob_course_id):
        indi_course={"CourseDetail":Database.get_course_details(glob_course_id)}
        return indi_course
    def get_qp_for_course():
        qp_t={"Qp":Database.get_qp_course()}
        return qp_t

    def qp_list(qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        qp_l=Database.qp_list(qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return qp_l
    def add_qp(qp_name,qp_code,user_id,is_active,qp_id):
        popupMessage = {"PopupMessage": Database.add_qp_details(qp_name,qp_code,user_id,is_active,qp_id)}    
        return popupMessage
    def get_qp(glob_qp_id):
        indi_qp={"QpDetail":Database.get_qp_details(glob_qp_id)}
        return indi_qp

    def question_type_list(question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        question_type_l = Database.question_type_list(question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return question_type_l
    def add_question_type(question_type_name,user_id,is_active,question_type_id):
        popupMessage = {"PopupMessage": Database.add_question_type_details(question_type_name,user_id,is_active,question_type_id)}    
        return popupMessage
    def get_question_type(glob_question_type_id):
        indi_question_type={"QuestionTypeDetail":Database.get_question_type_details(glob_question_type_id)}
        return indi_question_type

    def section_type_list(section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        section_type_l = Database.section_type_list(section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return section_type_l
    def add_section_type(section_type_name,user_id,is_active,section_type_id):
        popupMessage = {"PopupMessage": Database.add_section_type_details(section_type_name,user_id,is_active,section_type_id)}    
        return popupMessage
    def get_section_type(glob_section_type_id):
        indi_section_type={"SectionTypeDetail":Database.get_section_type_details(glob_section_type_id)}
        return indi_section_type
    
    def section_list(section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        section_l = Database.section_list(section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return section_l
    def add_section(section_name,section_type_id,p_section,user_id,is_active,section_id):
        popupMessage = {"PopupMessage": Database.add_section_details(section_name,section_type_id,p_section,user_id,is_active,section_id)}    
        return popupMessage
    def get_section(glob_section_id):
        indi_section={"SectionDetail":Database.get_section_details(glob_section_id)}
        return indi_section
    def all_section_types():
        section_types={"SectionTypes":Database.all_section_types()}
        return section_types
    def all_parent_section():
        p_sections={"P_Sections":Database.all_parent_section()}
        return p_sections

    # def state_and_district_list(state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
    #     state_and_district_list_l = Database.state_and_district_list_list(state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    #     return state_and_district_list_l

    def all_session_plan(course_id):
        SessionPlans = {"SessionPlans" : Database.all_session_plan(course_id)}
        return SessionPlans
    def all_module(session_plan_id):
        Modules = {"Modules": Database.all_module(session_plan_id),"Module_order": Database.module_order_for_session_plan(session_plan_id)}
        return Modules
    def get_session_order_for_module(module_id):
        Session_order = { "Session_order": Database.get_session_order_for_module(module_id), "SessionCode" : Database.sessioncode_for_module(module_id)}
        return Session_order
    def module_session_list(session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        session_l = Database.module_session_list(session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return session_l
    def add_session_plan(session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id):
        popupMessage = {"PopupMessage": Database.add_session_plan(session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id)}    
        return popupMessage
    def add_module(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id):
        popupMessage = {"PopupMessage": Database.add_module(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)}    
        return popupMessage
    def add_edit_session(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration):
        popupMessage = { "PopupMessage" : Database.add_edit_session(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration)}
        return popupMessage
    def get_session_detail(session_id):
        indi_session={"SessionDetail":Database.get_session_detail(session_id)}
        return indi_session