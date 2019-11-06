from Database import Database
class Candidate:
    def candidate_list(candidate_id,course_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        candidate_l = Database.candidate_list(candidate_id,course_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return candidate_l