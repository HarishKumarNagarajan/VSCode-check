from Database import Database
class Batch:
    def batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_batch(batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active):
        popupMessage = {"PopupMessage": Database.add_batch_details(batch_id,batch_name,course_id,center_id,trainer_id,center_manager_id,start_date,end_date,start_time,end_time,user_id,is_active)}
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