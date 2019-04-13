""" Todo List web based app """
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms import validators
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cross site forgery prevention key'
bootstrap = Bootstrap(app)


class SaveForm(FlaskForm):
    save = SubmitField('Save Data')


class ToDoForm(FlaskForm):
    description = StringField('What is the task description',
                              [validators.DataRequired()])
    email = EmailField('What is your email',
                       [validators.DataRequired(), validators.Email()])
    priority = SelectField('What is the priority',
                           choices=[('High', 'High'),
                                    ('Medium', 'Medium'),
                                    ('Low', 'Low')])
    submit = SubmitField('Add To Do Item')


class ClearForm(FlaskForm):
    clear = SubmitField('Clear')


class Task(object):
    def __init__(self, description, email, priority):
        self.description = description
        self.email = email
        self.priority = priority

    def set_description(self, text):
        self.description = text
        return self.text

    def set_email(self, text):
        self.email = text
        return self.email

    def set_priority(self, text):
        self.priority = text
        return self.priority

    def get_list(self):
        return self.description, self.email, self.priority


class ToDoList(object):
    def __init__(self):
        self.todolist = []
        self.listfile = 'list.bin'
        if self.listfile:
            self.load_list(self.listfile)

    def add_item(self, task):
        self.todolist.append(task)

    def clear_list(self):
        self.todolist = []

    def delete_item(self, task):
        try:
            self.todolist.remove(task)
        except ValueError:
            print "Task not in list"

    def save_list(self):
        try:
            with open(self.listfile, 'wb') as lfile:
                pickle.dump(self.todolist, lfile)
        except IOError:
            pass

    def load_list(self, listfile):
        try:
            with open(self.listfile, 'rb') as lfile:
                self.todolist = pickle.load(lfile)
        except IOError:
            pass

    def get_list(self):
        return self.todolist


@app.route('/')
def index():
    todo_form = ToDoForm()
    clear_form = ClearForm()
    save_form = SaveForm()
    return render_template('todo.html',
                           todo_form=todo_form,
                           clear_form=clear_form,
                           save_form=save_form,
                           tasklist=tasklist.get_list())


@app.route('/save', methods=['POST'])
def save():
    todo_form = ToDoForm()
    clear_form = ClearForm()
    save_form = SaveForm()
    if save_form.validate_on_submit():
        tasklist.save_list()
        return redirect(url_for('index'))
    return render_template('todo.html',
                           todo_form=todo_form,
                           clear_form=clear_form,
                           save_form=save_form,
                           tasklist=tasklist.get_list())


@app.route('/submit', methods=['POST'])
def submit():
    todo_form = ToDoForm()
    clear_form = ClearForm()
    save_form = SaveForm()
    if todo_form.validate_on_submit():
        tasklist.add_item(Task(todo_form.description.data,
                               todo_form.email.data,
                               todo_form.priority.data))
        return redirect(url_for('index'))
    return render_template('todo.html',
                           todo_form=todo_form,
                           clear_form=clear_form,
                           save_form=save_form,
                           tasklist=tasklist.get_list())


@app.route('/clear', methods=['POST'])
def clear():
    todo_form = ToDoForm()
    clear_form = ClearForm()
    save_form = SaveForm()
    if clear_form.validate_on_submit():
        tasklist.clear_list()
        return redirect(url_for('index'))
    return render_template('todo.html',
                           todo_form=todo_form,
                           clear_form=clear_form,
                           save_form=save_form,
                           tasklist=tasklist.get_list())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(405)
def unauthorized_error(e):
    return render_template('405.html'), 405


if __name__ == "__main__":
    tasklist = ToDoList()
    app.run()
