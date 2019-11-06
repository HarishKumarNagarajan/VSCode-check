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
    def add_course(course_name,project_id,user_id,is_active,center_ids,course_id,items):
        if items == "[]":
            popupMessage = {"PopupMessage": Database.add_course_details(course_name,project_id,user_id,is_active,center_ids,course_id,'')}
            return popupMessage
        else:
            popupMessage = {"PopupMessage": Database.add_course_details(course_name,project_id,user_id,is_active,center_ids,course_id,items)}
            return popupMessage
    def get_course(glob_course_id):
        indi_course={"CourseDetail":Database.get_course_details(glob_course_id)}
        return indi_course
