from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
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
    Task = StringField('Name', validators=[InputRequired()])
    TaskDesc = TextAreaField('Description', validators=[InputRequired(), Length(max=100)])

    

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
                    elif len(str(taskcheck[i])) > 90:
                        taskcheck[i] = taskcheck[i][:30] + "- " + taskcheck[i][30:60] + "- " + taskcheck[i][60:90] + "- " + taskcheck[i][90:]
                    task_desc = " ".join(taskcheck)
                    
                DataStoreTasks[task] = task_desc
                print(DataStoreTasks)  # For debugging purposes
            else:
                print("Task or TaskDesc is missing")  # Debugging message for missing data
            
            with open ('TaskStorage.json', 'w') as f:
                json.dump(DataStoreTasks, f)
            return render_template('Page_2.html', form=form, DataStoreTasks=DataStoreTasks)
    
    return render_template('Page_2.html', form=form, DataStoreTasks=DataStoreTasks)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        button_value = request.form.get('login')
        button_value2 = request.form.get('Register')
        if button_value == 'Login':
            usernameentered = request.form.get('username')
            passwordentered = request.form.get('password')
            try:
                with open ("User&Pass.json", "r") as f:
                    userdata = json.load(f)
                if usernameentered in userdata.keys():
                    if passwordentered == userdata[usernameentered]:
                        return render_template('Page_1.html')
                    else:
                        return render_template('Login.html')
                else:
                    return render_template('Login.html')
            except json.decoder.JSONDecodeError:
                print("No data in file")
                pass
        elif button_value2 == 'Register':
            return render_template('Register.html', href='/Register')
        
    # If GET or no recognized button value, stay on the login page or handle accordingly
    return render_template('Login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        button_value = request.form.get('Register')
        if button_value == 'Register':
            usernameentered = request.form.get('username')
            passwordentered = request.form.get('password')
            with open ("User&Pass.json", "r") as f:
                try:
                    userdata = json.load(f)
                except json.decoder.JSONDecodeError:
                    userdata = {}
                    
            try:
                    
                if usernameentered in userdata.keys():
                    print("Username already exists")
                
            except json.decoder.JSONDecodeError:
                pass
            
            except Exception as e:
                print(f"Data error:")
                print(e)
            
            userdata[usernameentered] = passwordentered
            with open ("User&Pass.json", "w") as f:
                json.dump(userdata, f)
            return render_template('Login.html')
    
        elif button_value == 'Login':
                return render_template('Login.html')

    # If GET or no recognized button value, stay on the login page or handle accordingly
    return render_template('Register.html')
            
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
    app.run(debug=True)