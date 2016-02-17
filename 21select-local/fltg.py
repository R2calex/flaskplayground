#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
select widget - local list - for small lists like shift: day night afternoon.
I have used enum with other systems.

ref.
https://gist.github.com/mrjoes/3714266
http://stackoverflow.com/questions/31081516/how-can-i-turn-a-string-model-field-into-a-select-input-in-flask-admin
http://w3foverflow.com/question/flask-admin-form_override-selectfield-form_args-from-another-view-as-an-in-line-model/

'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import Column, Integer, String, ForeignKey, String, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_admin.form.widgets import Select2Widget
from wtforms import SelectField

# Create application
app = Flask(__name__)
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '12344567901'
# define db engine..
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#connect and  reflect...
connection = db.engine.connect()
# no need to reflect view...
db.metadata.reflect(bind=db.engine, only=['users','Persons'])
Base = declarative_base()
metadata = Base.metadata

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#reflect table...   
class users(db.Model):
    __table__ = db.Table('users', db.metadata,
        autoload=True, autoload_with=db.engine
    )
   
class Person(db.Model):
    __table__ = db.Table('Persons', db.metadata,
        autoload=True, autoload_with=db.engine
    )
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# customize views..
  
class dvview(ModelView):
    column_display_pk = True

class persons_view(dvview):
    form_overrides = dict(City=SelectField)
    form_args = dict(City=dict(choices=[
                ('', 'Please Select'),
                ('London', 'London'),
                ('Kitchener', 'Kitchener')
            ]
        )
    )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create admin
admin = admin.Admin(app, name='fltg 21selectlocal', template_mode='bootstrap3')

admin.add_view(dvview(users, db.session))
admin.add_view(persons_view(Person, db.session))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    # Start app
    app.run(host='0.0.0.0', port=5000, debug=True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
