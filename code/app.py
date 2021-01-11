from flask import Flask, request, url_for, redirect, render_template, session
import allow_utils
import allow_conn
import json

app = Flask(__name__)

@app.route('/')
def app_index():
    return render_template('index.html')


@app.route('/current_values')
def current_values():

    data = allow_utils.get_current_values()
    cur_date = data[0][0]
    for row in data:
        if row[1] == 'MICAH':
            mVal = row[2]
        elif row[1] == 'CAMERON':
            cVal = row[2]
        elif row[1] == 'ALEX':
            aVal = row[2]
        else:
            raise Exception("Name not found")

    
    return render_template('currentValues.html', WEEK_END_DATE=cur_date, MICAH=mVal, CAMERON=cVal, ALEX=aVal)

@app.route('/modifyValues', methods=['GET','POST'])
def modifyValues():
    if request.method == 'POST':
        #get values from the form
        child = "'"+request.values.get('childSelect')+"'"
        amount = request.values.get('modifyAmount')
        reason = "'"+request.values.get('modifyReason')+"'"
        #grab the current date
        cur_date = "'"+allow_utils.get_current_weekend()+"'"
        #prepare the insert statement to update the amount
        sql = """
        insert into amount_details values({}, {}, {}, {})
        """.format(cur_date, child, amount, reason)
        #execute the statement and check teh results
        result = allow_conn.execute_statement(sql)
        if result['code'] == 0:
            message = 'You have successfully modified the allowance for {} by ${}'.format(child, amount)
        else:
            message = result['message']
        return redirect(url_for('message', message=message))


    cur_date = allow_utils.get_current_weekend()
    return render_template('modifyValues.html', WEEK_END_DATE=cur_date)

@app.route('/finalizeWeek', methods=['GET','POST'])
def finalizeWeek():
    cur_date = allow_utils.get_current_weekend()    
    next_date = allow_utils.get_next_weekend()
    if request.method == 'POST':
        #format the current date
        cur_date_str = "'"+cur_date+"'"
        next_date_str = "'"+next_date+"'"
        #prepare the update and insert statements and run them to finalize the week and initialize the next
        update_sql = """
        update weekends set current_record_ind = 'N' 
        where week_end_date = {};
        update weekends set current_record_ind = 'Y'
        where week_end_date = {};
        """.format(cur_date_str, next_date_str)
        #execute the statement and check teh results
        result = allow_conn.execute_statement(update_sql)
        if result['code'] == 0:
            #initialize the new week
            init_sql = """
            insert into amount_details (week_end_date, child_name, modified_amount, modify_reason)
            (select w.week_end_date, da.child_name, da.amount, 'Starting Amount' as modify_reason
            from weekends w
            , def_allow da
            where w.current_record_ind = 'Y')
            """
            #execute the statement and check the results
            init_result = allow_conn.execute_statement(init_sql)
            if init_result['code'] == 0:
                message = "The week of {} has been finalized and the week of {} has been initialized".format(cur_date, next_date)
            else:
                message = "The week was finalized, however the new week could not be initialized.  Please contact the admin for support."
        else:
            message = result['message']
        return redirect(url_for('message', message=message))



    return render_template('finalizeWeek.html', WEEK_END_DATE=cur_date)


@app.route('/priorActivity', methods=['GET','POST'])
def priorActivity():
    
    #if the request is a post request grab the options and return the activity for that date and child
    if request.method == 'POST':
        # #get values from the form
        child = "'"+request.values.get('childSelect')+"'"
        cur_date = "'"+request.values.get('dateSelect')+"'"

        message = '{"date":"{}","child":"{}"}'.format(cur_date, child)
        return redirect(url_for('showActivity', message=message))

    #get list of prior dates
    get_date_list_sql = """
    select week_end_date from weekends
    where week_end_date < (
        Select week_end_date from weekends where current_record_ind = 'Y'
        )
    order by week_end_date desc
    limit 10;
    """
    #execute query and place dates in list
    date_rows = allow_conn.execute_query(get_date_list_sql)
    date_list = [str(row[0]) for row in date_rows]
    date_len = len(date_list)

    #if the request is a get render the page with the appropriate options
    return render_template('priorActivity.html', date_list = date_list, date_len = date_len)

@app.route('/message')
def message():
    message = request.args['message']

    return render_template('message.html', MESSAGE_TEXT=message)

@app.route('/showActivity')
def showActivity():
    str_message = request.args['message']
    msg_dict = json.loads(str_message)
    cur_date = msg_dict['date']
    cur_child = msg_dict['child']
    # #determine if we need all children or just a specific kid
    # if cur_child == 'ALL':
    #     sql_where = "\n WHERE week_end_date = '{}'".format(cur_date)
    # else:
    #     sql_where = "\n WHERE week_end_date = '{}' and child_name = '{}'".format(cur_date, child)
    # #prepare the query to grab the activity
    # act_sql = """
    # select week_end_date, child_name, modified_amount, modify_reason 
    # from amount_details 
    # {} 
    # order by child_name
    # """.format(sql_where)
    # #execute the statement and check teh results
    # act_rows = allow_conn.execute_query(act_sql)
    # parse results into the
    activity_list = [('date', 'kid', 'amount', 'reason'), ('date1', 'kid1', 'amount1', 'reason1')]
    activity_len = len(activity_list)
    return render_template('showActivity.html', cur_date = cur_date, cur_child = cur_child, activity = activity_list, len = activity_len)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
