'''
Create a Flask application with three routes:

Route 1: Display a welcome message on the home page.
Route 2: Display information about yourself on a separate page.
Route 3: Create a custom 404 error page.

Form Handling:
Create a form with Flask that takes user input (e.g., name, email) and displays it on a new page after submission.

Static files:
Add a CSS file to your Flask project and style your HTML pages.
Use the url_for function to include the CSS file in your templates.

File Upload:
Create a Flask route that allows users to upload files. Save the uploaded files on the server and display a list of uploaded files on another page.


API Endpoint:
Create a simple RESTful API using Flask. Implement endpoints for GET, POST, and DELETE operations on a resource (e.g., a list of tasks).


'''

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, jsonify
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        return render_template('form_result.html', name=name, email=email)
    return render_template('form.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=files)

# API Endpoint: Simple RESTful API for managing tasks
tasks = []
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
#curl http://localhost:5000/tasks
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if 'task' in data:
        new_task = data['task']
        tasks.append(new_task)
        return jsonify({'message': 'Task added successfully'})
    else:
        return jsonify({'error': 'Invalid request. Please provide a task in the request body.'}), 400
#curl -X POST -H "Content-Type: application/json" -d '{"task":"New task"}' http://localhost:5000/tasks
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id < len(tasks):
        del tasks[task_id]
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
