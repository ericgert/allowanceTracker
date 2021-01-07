from flask import Flask, request, url_for, redirect, render_template
import allow_utils


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
        child = request.values.get('childSelect')
        amount = request.values.get('modifyAmount')
        message_text = 'You have successfully modified the allowance for {} by {}'.format(child, amount)
        return redirect(url_for('message', message=message_text))


    cur_date = allow_utils.get_current_weekend()
    return render_template('modifyValue.html', WEEK_END_DATE=cur_date)

@app.route('/message')
def message(message):
    message=message
    return render_template('message.html', MESSAGE_TEXT=message)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
