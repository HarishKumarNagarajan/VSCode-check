from flask_restful import Resource
from flask import request
from Models import Content

###########################################################3
class course_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_id = request.form['course_id'] 
            practice_id = request.form['practice_id']
            project_id = request.form['project_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Content.course_list(course_id,project_id,practice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class AllCenterList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllCenter()

class AllPracticeList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllPractice()


class AllProjectsBasedOnPractice(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            practice_id = request.form['practice_id']
            project_id = request.form['project_id']
            return Content.AllProjectOnPractice(project_id,practice_id) 


