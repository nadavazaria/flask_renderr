from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from icecream import ic
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db' 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    
app.config["CHECK_SAME_THREAD"] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(50),nullable = False)
    last_name= db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(501))
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    email = db.Column(db.String(50),nullable = False,unique =True)
    orders = db.relationship('Order',backref = 'customer') 

  

order_product = db.Table('order_product',
    db.Column('order_id',db.Integer,db.ForeignKey('order.id'),primary_key = True),
    db.Column('product_id',db.Integer,db.ForeignKey('product.id'),primary_key = True)
    )

class Order(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    order_date =db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    shop_date = db.Column(db.DateTime,nullable = True)
    delivered_date = db.Column(db.DateTime,nullable = True)
    coupon_code = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable = False)
    products =db.relationship('Product',secondary = order_product)


class Product(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name =db.Column(db.String(50),unique = True,nullable = False)
    price = db.Column(db.Float(50),nullable = False)


@app.route("/")
def home():
    with app.app_context():
            db.create_all()
        
    customers = [
            {'name': 'nadav', 'last_name': 'azaria', 'email': 'nadav.azaria98@gmail.com', 'address': 'nehemia 140', 'city': 'reshon lezion'},
            {'name': 'adi', 'last_name': 'azaria', 'email': 'adi.azaria@gmail.com', 'address': 'nehemia 140', 'city': 'reshon lezion'},
            {'name': 'bella', 'last_name': 'azaria', 'email': 'bella.azaria@gmail.com', 'address': 'nehemia 140', 'city': 'reshon lezion'}
        ]
        
    for customer_info in customers:
            # Check if a customer already exists with the given email
        if not Customer.query.filter_by(email=customer_info['email']).first():
                # If not, create and add the new customer
            new_customer = Customer(
            name=customer_info['name'],
            last_name=customer_info['last_name'],
            email=customer_info['email'],
            address=customer_info['address'],
            city=customer_info['city']
        )
        db.session.add(new_customer)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to add customers: {str(e)}"}

        # Example of querying a specific customer
        nadav = Customer.query.filter_by(email="nadav.azaria98@gmail.com").first()
        if nadav:
            return {"name": nadav.name, "email": nadav.email}
        else:
            return {"error": "Specified customer not found."}


if __name__ == "__main__":
    with app.app_context():
        ic('found context')
        db.create_all()
        ic('this is after the craetion ')
    app.run(debug=True)
    

