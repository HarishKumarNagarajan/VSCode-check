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
    def add_center(center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name):
        popupMessage = {"PopupMessage": Database.add_center_details(center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name)}
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
    def get_all_BU():
        BU={"BU":Database.get_all_BU()}
        return BU
    def get_all_Cluster_Based_On_Region(region_id):
        Cluster={"ClusterOnRegion":Database.get_all_Cluster_Based_On_Region(region_id)}
        return Cluster

    def client_list(client_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        client_l = Database.client_list(client_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return client_l
    def add_client(client_name,client_code,user_id,is_active,client_id):
        popupMessage = {"PopupMessage": Database.add_client_details(client_name,client_code,user_id,is_active,client_id)}
        return popupMessage
    def get_client(glob_client_id):
        indi_client={"ClientDetail":Database.get_client_detail(glob_client_id)}
        return indi_client

    def region_list(region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        region_l = Database.region_list(region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return region_l
    def add_region(region_name,region_code,user_id,is_active,region_id):
        popupMessage = {"PopupMessage": Database.add_region_details(region_name,region_code,user_id,is_active,region_id)}
        return popupMessage
    def get_region(glob_region_id):
        indi_region={"RegionDetail":Database.get_region_detail(glob_region_id)}
        return indi_region

    
    def cluster_list(cluster_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        cluster_l = Database.cluster_list(cluster_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return cluster_l
    def add_cluster(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id):
        popupMessage = {"PopupMessage": Database.add_cluster_details(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id)}
        return popupMessage
    def get_cluster(glob_cluster_id):
        indi_cluster={"ClusterDetail":Database.get_cluster_detail(glob_cluster_id)}
        return indi_cluster
    def get_all_Region():
        Region={"Region":Database.get_all_Region()}
        return Region
    def sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        sub_center_l = Database.sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return sub_center_l
    def add_sub_center(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id):
        popupMessage = {"PopupMessage": Database.add_sub_center_details(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id)}
        return popupMessage
    def get_sub_center(glob_sub_center_id):
        indi_sub_center={"SubCenterDetail":Database.get_sub_center_detail(glob_sub_center_id)}
        return indi_sub_center