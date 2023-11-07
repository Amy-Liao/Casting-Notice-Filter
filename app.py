from flask import Flask, render_template, request, redirect, url_for
from auto_search.text_processing import extract_messages_from_file

app = Flask(__name__)

@app.route('/')
def index():
    form_data = ('Female', '', '', '') 
    return render_template('index.html', form_data=form_data)

@app.route('/process_search_form', methods=['POST'])
def process_search_form():
    gender = 'F' if request.form['gender']=='Female' else 'M'
    search_date = request.form['search_date']
    age_lower = int(request.form['age_lower'])
    age_upper = int(request.form['age_upper'])
    uploaded_file = request.files['file_message']
    processed_data = extract_messages_from_file(uploaded_file, search_date, age_lower, age_upper, gender)
    form_data=(request.form['gender'], search_date, request.form['age_lower'], request.form['age_upper'])
    return render_template('index.html', processed_data=processed_data, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)