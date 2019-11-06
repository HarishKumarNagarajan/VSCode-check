from Database import Database
class Master:
    ##Center_type##
    def center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        center_type_l =Database.center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return center_type_l
    def add_center_type(center_type_name,user_id,is_active,center_type_id):
        popupMessage = {"PopupMessage": Database.add_center_type_details(center_type_name,user_id,is_active,center_type_id)}
        return popupMessage
    def get_center_type(glob_center_type_id):
        indi_center_type={"CenterTypeDetail":Database.get_center_type_details(glob_center_type_id)}
        return indi_center_type
    
    ##Center_Category##
    def center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        center_category_l = Database.center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return center_category_l
    def add_center_category(center_category_name,user_id,is_active,center_category_id):
        popupMessage = {"PopupMessage": Database.add_center_category_details(center_category_name,user_id,is_active,center_category_id)}
        return popupMessage
    def get_center_category(glob_center_category_id):
        indi_center_type={"CenterCategoryDetail":Database.get_center_category_details(glob_center_category_id)}
        return indi_center_type

    ##Center##
    def center_list(center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        center_l = Database.center_list(center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return center_l
    def add_center(center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name):
        popupMessage = {"PopupMessage": Database.add_center_details(center_name,user_id,is_active,center_id,center_type_id,center_category_id,country_id,satet_id,district_id,location_name)}
        return popupMessage
    def AllCenters(glob_center_id):
        indi_center={"CenterDetail":Database.GetCenter(glob_center_id)}
        return indi_center
    def AllCenterTypes():
        center_t={"Center_Types":Database.GetCenterType()}
        return center_t
    def AllCenterCategory():
        center_categories={"Center_Categories":Database.GetCenterCategory()}
        return center_categories
    def AllCountry():
        countries_for={"Countries":Database.GetCountry()}
        return countries_for
    def AllStatesOnCountry(country_id):
        states_for_country={"States":Database.GetStatesBasedOnCountry(country_id)}
        return states_for_country
    def AllDistrictsOnState(state_id):
        districts_for_state={"Districts":Database.GetDistrictsBasedOnStates(state_id)}
        return districts_for_state