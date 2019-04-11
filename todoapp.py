from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cross site forgery prevention key'
bootstrap = Bootstrap(app)


class ToDoForm(Form):
    description = StringField('What is the task description',
                              validators=[DataRequired()])
    email = StringField('What is your email',  validators=[DataRequired()])
    priority = SelectField('What is the priority',
                           choices=[('High', 'high'),
                                    ('Medium', 'medium'),
                                    ('Low', 'low')])
    submit = SubmitField('Submit')


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


@app.route('/', methods=['GET', 'POST'])
def index():
    l1 = []
    l1.append(Task('Task 1', 'mike@test.com', 'High'))
    l1.append(Task('Task 2', 'tstes@kjfas.com', 'Low'))
    form = ToDoForm()
    if form.validate_on_submit():
        l1.append(Task(form.description.data,
                       form.email.data,
                       form.priority.data))
    return render_template('todo.html', form=form, tasklist=l1)


@app.route('/user/<name>')
def user(name):
    return '<h1> Hello, %s!</h1>' % name


if __name__ == "__main__":
    app.run()
