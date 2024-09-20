from flask import Flask, request, render_template
import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length
import json
from subprocess import Popen
#UTILISE POPEN MULTITHREADING FOR THE APP READER SCRIPT

try:
    Popen("python AppReader_Remake_Testing.py")
except:
    pass
DataStoreTasks = {}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the key oooh'

class TaskForm(FlaskForm): 
    Task = StringField('Name', validators=[InputRequired(), Length(max=50)])
    TaskDesc = TextAreaField('Description', validators=[InputRequired(), Length(max=200)])

    

@app.route('/Page_1/', methods=['POST', 'GET'])
def page_1():
    if request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'Page 2':
            form = TaskForm()
            return render_template('Page_2.html', form=form, DataStoreTasks=DataStoreTasks)
    return render_template('Page_1.html')



@app.route('/Page_2/', methods=['POST', 'GET'])
def page_2():
    form = TaskForm()
    
    if request.method == 'POST':
        button_value = request.form.get('button')
        if button_value == 'Page 1':
            return render_template('Page_1.html')
        elif button_value == 'submit':
            # Extract form data into the DataStoreTasks dictionary
            task = request.form.get('Task')
            task_desc = request.form.get('TaskDesc')
            if task and task_desc:
                taskcheck = task_desc.split(" ")
                for i in range(len(taskcheck)):
                    if len(str(taskcheck[i])) < 30:
                        pass
                    elif len(str(taskcheck[i])) > 30 and len(str(taskcheck[i])) < 60:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:]
                    elif len(str(taskcheck[i])) > 60 and len(str(taskcheck[i])) < 90:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:]
                    elif len(str(taskcheck[i])) > 90 and len(str(taskcheck[i])) < 120:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:90] + "- " + taskcheck[i][90:]
                    elif len(str(taskcheck[i])) > 120 and len(str(taskcheck[i])) < 150:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:90] + "- " + taskcheck[i][90:120] + "- " + taskcheck[i][120:]
                    elif len(str(taskcheck[i])) > 150 and len(str(taskcheck[i])) < 180:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:90] + "- " + taskcheck[i][90:120] + "- " + taskcheck[i][120:150] + "- " + taskcheck[i][150:]
                    elif len(str(taskcheck[i])) > 180:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:90] + "- " + taskcheck[i][90:120] + "- " + taskcheck[i][120:150] + "- " + taskcheck[i][150:180] + "- " + taskcheck[i][180:]
                    task_desc = " ".join(taskcheck)
                    
                DataStoreTasks[task] = task_desc
            else:
                print("Task or TaskDesc is missing")  # Debugging message for missing data
            
            with open ('TaskStorage.json', 'w') as f:
                json.dump(DataStoreTasks, f)
            return render_template('Page_2.html', form=form, DataStoreTasks=DataStoreTasks)
    
    return render_template('Page_2.html', form=form, DataStoreTasks=DataStoreTasks)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    with open ('TaskStorage.json', 'w') as f:
        json.dump(DataStoreTasks, f)
    return render_template('Dashboard.html', DataStoreTasks=DataStoreTasks)

            
@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.get_json()
    task = data.get('task')

    if task in DataStoreTasks:
        del DataStoreTasks[task]
        with open('TaskStorage.json', 'w') as f:
            json.dump(DataStoreTasks, f)
        return {'status': 'success'}, 200
    else:
        return {'status': 'task not found'}, 404

if __name__ == '__main__':
    try:
        with open ('TaskStorage.json', 'r') as f:
            DataStoreTasks = json.load(f)
    except:
        print('No data in file')

    os.system('cls')
    print("")
    print("Welcome to AppScan - The Personal Support Tool")
    print("To leave the program, please close the window.")
    print("To have the program running in the background, please leave the window running")
    print("To access the data display webapp, visit http://127.0.0.1:5000/dashboard")
    print("")
    app.run()