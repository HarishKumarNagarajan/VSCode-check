from flask_restful import Resource
from flask import request
from Models import Master           

###########################################################3
class center_list(Resource):
    @staticmethod
    def post():
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


class all_districts_based_on_state(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            state_id=request.form['state_id']
            return Master.AllDistrictsOnState(state_id)


class all_states_based_on_country(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            country_id=request.form['country_id']
            return Master.AllStatesOnCountry(country_id)



class all_countries(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCountry()


class all_center_categories(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCenterCategory()


class all_center_type(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCenterTypes()

