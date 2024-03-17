from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE__URI'] = "mysql://'root':1234@localhost/garage"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class customer(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50),unipue = True,nullable = False)
    cars = db.relationship('Car',backref = 'customer')

class Car(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    car_model = db.Column(db.Integer)
    car_maker = db.Column(db.String(50))
    car_color = db.Column(db.String(50))
    customer_id = db.Column(db.integer,db.ForeginKey('customr.id'),nullable = False)




if __name__ == "__main__":
    with app.app_context():
        db.create.all()
    app.run(debug=True,port=5500)




