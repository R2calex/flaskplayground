'''
Small-Example: custom view
David Gleba.
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib import sqla
from wtforms import SelectField

app = Flask(__name__)  # Create application
app.config['SECRET_KEY'] = '123456790'  # Create dummy secrey key so we can use sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite' # Create database
db = SQLAlchemy(app)

@app.route('/')  # Flask views
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

from flask_admin import BaseView, expose
class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('analytics.html')
    
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))
    cartype = db.Column(db.String(50))

class CarAdmin(sqla.ModelView):
    form_overrides = dict(cartype=SelectField)
    form_args = dict(cartype=dict(choices=[
                ('', 'Please Select'),
                ('Compact', 'Compact'),
                ('Mid-size', 'Mid-size'),
                ('Pickup Truck', 'Pickup Truck')
            ]))

# Create admin
admin = admin.Admin(app, name='31form', template_mode='bootstrap3')
admin.add_view(AnalyticsView(name='Analytics', endpoint='ana'))
admin.add_view(CarAdmin(Car, db.session))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
