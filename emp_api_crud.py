""" Importing Packages and Classes """

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate


""" Setting up the Flask application """
app = Flask(__name__)


""" App configuration """
app.config['SECRET_KEY'] = 'mysecretkey'


""" Setting up the path for database """
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')

""" Database configuration """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


""" Database Creation """
db = SQLAlchemy(app)
Migrate(app, db)

""" api call """
api = Api(app)


""" Database Model """


class Employee_db(db.Model):
    name = db.Column(db.String(100), primary_key=True)

    def __init__(self, name):
        self.name = name

    """ Returns object in JSON format """

    def json(self):
        return {'name': self.name}


""" Api CRUD Methods """


class Employee(Resource):

    """ CREATE Method """

    def post(self, name):

        try:
            emp = Employee_db(name=name)

            db.session.add(emp)
            db.session.commit()

            return emp.json()

        except:

            return {'note': f'Employee {name} Already Found'}, 404

    """ READ Method """

    def get(self, name):

        emp = Employee_db.query.filter_by(name=name).first()

        if emp:
            return emp.json()

        else:
            return {'note': f'Employee {name} Not Found'}, 404

    """ Delete Method """

    def delete(self, name):

        try:
            emp = Employee_db.query.filter_by(name=name).first()

            db.session.delete(emp)
            db.session.commit()

            return {'note': f'Employee {name} Deleted successfully'}, 404

        except:
            return {'note': f'Employee {name} not Found'}, 404


class AllEmployees(Resource):

    def get(self):

        employees = Employee_db.query.all()

        op = [emp.json() for emp in employees]

        if op:
            return op

        else:
            return {'note': 'No Employees Found'}


""" Adding Resource to the Api """

api.add_resource(Employee, '/employee/<string:name>')
api.add_resource(AllEmployees, '/employees')


if __name__ == '__main__':
    app.run(debug=True)
