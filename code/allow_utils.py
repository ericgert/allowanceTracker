import allow_conn as con
import datetime

def get_current_weekend():
    current_date =  con.execute_query("Select week_end_date from weekends where current_record_ind = 'Y';")
    return str(current_date[0][0])


def get_current_values():
    query_sql = """
    SELECT week_end_date, child_name, amount
    FROM allowance_details
    WHERE week_end_date = (
	    select week_end_date 
	    from weekends
	    where current_record_ind = 'Y'
	    )
    ;
    """
    rows = con.execute_query(query_sql)
    return rows


