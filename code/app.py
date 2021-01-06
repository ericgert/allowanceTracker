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

    
    return render_template('currentValues.html', WEEK_END_DATE=cur_date MICAH=mVal, CAMERON=cVal, ALEX=aVal)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
