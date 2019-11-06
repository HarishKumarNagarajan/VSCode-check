from Database import Database
class UsersM:
    def user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_user_role(user_role_name,user_id,is_active,user_role_id):
        popupMessage = {"PopupMessage": Database.add_user_role_details(user_role_name,user_id,is_active,user_role_id)}
        return popupMessage
    def get_user_role(glob_user_role_id):
        indi_user_role={"UserRoleDetail":Database.get_user_role_details(glob_user_role_id)}
        return indi_user_role
    def user_list(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.user_list(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def add_user(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager):
        popupMessage = {"PopupMessage": Database.add_user_details(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,center_ids,is_reporting_manager)}
        return popupMessage
    def AllUserRole():
        userrole_list={"UserRoles":Database.GetUserRole()}
        return userrole_list
    def get_user(glob_user_id):
        indi_user={"UserDetail":Database.get_user_details(glob_user_id)}
        return indi_user