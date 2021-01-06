from flask import Flask, request, url_for, redirect, render_template
app = Flask(__name__)

@app.route('/')
def app_index():
    return render_template('index.html')


@app.route('/current_values')
def current_values():
    cVal = 3.00
    aVal = 2.00
    mVal = 1.50
    
    return render_template('currentValues.html', mVal=mVal, cVal=cVal, aVal=aVal)
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
