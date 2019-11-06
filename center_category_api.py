from flask_restful import Resource
from flask import request
from Models import Master


############################################################
class center_category_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_category_id = request.form['center_category_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)


