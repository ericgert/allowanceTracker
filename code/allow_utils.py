import allow_conn as con

def get_current_weekend():
    current_date =  con.execute_query("Select week_end_date from weekends where current_record_ind = 'Y';")
    return current_date
