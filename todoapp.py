""" Todo List web based app """
import pickle
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms import validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cross site forgery prevention key'
bootstrap = Bootstrap(app)


class ToDoForm(FlaskForm):
    """ A Flask derived form with validators imported to ensure that
    form fields are not empty, and fit the required validation
    (email regex) """
    description = StringField('What is the task description',
                              [validators.DataRequired()])
    email = EmailField('What is your email',
                       [validators.DataRequired(), validators.Email()])
    priority = SelectField('What is the priority',
                           choices=[('High', 'High'),
                                    ('Medium', 'Medium'),
                                    ('Low', 'Low')])
    submit = SubmitField('Add To Do Item')


class SaveForm(FlaskForm):
    """ Flask form to allow us to set a save button """
    save = SubmitField('Save Data')


class ClearForm(FlaskForm):
    """ Flask form to allow us to set a clear button """
    clear = SubmitField('Clear')


class Task(object):
    """ A task has a description, email and priority fields """
    def __init__(self, description, email, priority):
        self.description = description
        self.email = email
        self.priority = priority

    def set_description(self, text):
        """ Setter for description field """
        self.description = text
        return self.description

    def get_description(self):
        """ Getter for description field """
        return self.description

    def set_email(self, text):
        """ Setter for email field """
        self.email = text
        return self.email

    def set_priority(self, text):
        """ Setter for priority field """
        self.priority = text
        return self.priority

    def get_task(self):
        """ Returns a tuple of the current task object """
        return self.description, self.email, self.priority


class ToDoList(object):
    """ A todo list is a list of task objects """
    def __init__(self):
        self.todolist = []
        self.listfile = 'list.bin'
        if self.listfile:
            self.load_list()

    def add_item(self, task):
        """ Adds a new task object to our list """
        self.todolist.append(task)

    def clear_list(self):
        """ Reverts our list back to it's original, clear state """
        self.todolist = []

    def delete_item(self, description):
        """ Attempts to remove the object from the list, if it exists """
        try:
            for task in self.todolist:
                if task.get_description() == description:
                    self.todolist.remove(task)
        except ValueError:
            print "Task not in list"

    def save_list(self):
        """ Pickles the list, saving the list of task objects to a file """
        try:
            with open(self.listfile, 'wb') as lfile:
                pickle.dump(self.todolist, lfile)
        except IOError:
            pass

    def load_list(self):
        """ Loads the task objects from a file to the tasklist """
        try:
            with open(self.listfile, 'rb') as lfile:
                self.todolist = pickle.load(lfile)
        except IOError:
            pass

    def get_list(self):
        """ Getter - returns the list object """
        return self.todolist


@app.route('/')
def index():
    """ Main index page - no actions allowed in this branch """
    todo_form = ToDoForm()
    clear_form = ClearForm()
    save_form = SaveForm()
    return render_template('todo.html',
                           todo_form=todo_form,
                           clear_form=clear_form,
                           save_form=save_form,
                           tasklist=tasklist.get_list())


@app.route('/delete', methods=['POST'])
def delete():
    tasklist.delete_item(request.form.get('delete_task'))
    tasklist.save_list()
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save():
    """ Save branch - gets the action from the save_form button, and
    performs the tasklist.save_list function"""
    tasklist.save_list()
    return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit():
    """ Submit branch - validates the form data on the todo_form
    and, if validated, creates a task object with the form data
    and appends it to the tasklist """
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        tasklist.add_item(Task(todo_form.description.data,
                               todo_form.email.data,
                               todo_form.priority.data))
        return redirect(url_for('index'))
    return render_template('todo.html',
                           todo_form=todo_form,
                           tasklist=tasklist.get_list())


@app.route('/clear', methods=['POST'])
def clear():
    """ Clear branch - sets the action to the clear form button
    to clear all fields and reset the list to it's original state """
    tasklist.clear_list()
    tasklist.save_list()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    """ Renders a custom 404 error page """
    print error
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """ Renders a custom 500 error page """
    print error
    return render_template('500.html'), 500


@app.errorhandler(405)
def unauthorized_error(error):
    """ Renders a custom 405 error page """
    print error
    return render_template('405.html'), 405


if __name__ == "__main__":
    tasklist = ToDoList()
    app.run()
