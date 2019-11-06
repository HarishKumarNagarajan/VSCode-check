from Database import Database
class Batch:
    def batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_batch(batch_id,batch_name,course_id,batch_code,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active,actual_start_date,actual_end_date):
        popupMessage = {"PopupMessage": Database.add_batch_details(batch_id,batch_name,course_id,batch_code,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active,actual_start_date,actual_end_date)}
        return popupMessage
    def get_batch(glob_batch_id):
        indi_batch={"BatchDetail":Database.get_batch_details(glob_batch_id)}
        return indi_batch
    def AllCourse():
        course_f={"Courses":Database.GetCourse()}
        return course_f
    def AllCenterOnCourse(course_id):
        centers_f={"Centers":Database.GetCenterBasedOnCourse(course_id)}
        return centers_f
    def AllTrainersOnCenter(center_id):
        trainers_f={"Trainers":Database.GetTrainersBasedOnCenter(center_id)}
        return trainers_f
    def AllCenterManagerOnCenter(center_id):
        centermanager_f={"CenterManager":Database.GetCenterManagerBasedOnCenter(center_id)}
        return centermanager_f
    def candidate_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.candidates_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_edit_candidate_batch(candidate_ids,batch_id,course_id,user_id):
        popupMessage = {"PopupMessage": Database.add_edit_map_candidate_batch(candidate_ids,batch_id,course_id,user_id)}
        return popupMessage