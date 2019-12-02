from flask import Flask, render_template, request, flash, send_file
import create_dendrogram
import io
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


@app.route('/')
def index():
    with open('./static/data/sample.csv') as file:
        data = create_dendrogram.get_json(file)
    return render_template('index.j2', data=data, tab='input')


@app.route('/', methods=['POST'])
def input_data():
    if request.method == 'POST':
        input_type = request.args.get('input_type')
        if input_type == 'input':
            try:
                data = create_dendrogram.get_json(request.form['text'], tab=True)
            except (TypeError, IndexError):
                data = None
            return render_template('index.j2', data=data, tab=input_type)
        elif 'file' not in request.files:
            flash('No file part')
            return render_template('index.j2', data=None, tab=input_type)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return render_template('index.j2', data=None, tab=input_type)
        if file and allowed_file(file.filename):
            f = request.files['file']
            stream = io.StringIO(f.stream.read().decode('UTF8'), newline=None)
            try:
                data = create_dendrogram.get_json(stream)
            except (TypeError, IndexError):
                data = None
            return render_template('index.j2', data=data, tab=input_type)
        else:
            flash('Allowed file type: CSV')
            return render_template('index.j2', data=None, tab=input_type)


@app.route('/favicon.ico')
def send_favicon():
    return send_file('favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)
