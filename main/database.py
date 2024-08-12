from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Models
class User(db.Model):
    __tablename__ = 'users'
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)

class Truck(db.Model):
    __tablename__ = 'trucks'
    TruckID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TruckNumberPlate = db.Column(db.String(50), nullable=False)
    DriverName = db.Column(db.String(50), nullable=False)
    DriverLicenseID = db.Column(db.String(50), nullable=False)
    DriverContact = db.Column(db.String(50), nullable=False)
    TruckRFID = db.Column(db.String(50), nullable=False)

class Store(db.Model):
    __tablename__ = 'stores'
    StoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StoreName = db.Column(db.String(100), nullable=False)
    StoreManager = db.Column(db.String(50), nullable=False)
    StoreContact = db.Column(db.String(50), nullable=False)
    StoreAddress = db.Column(db.String(200), nullable=False)

class SKU(db.Model):
    __tablename__ = 'skus'
    SKUID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SKUName = db.Column(db.String(100), nullable=False)
    WarehouseNumber = db.Column(db.String(50), nullable=False)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    AssignmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TruckID = db.Column(db.Integer, db.ForeignKey('trucks.TruckID'), nullable=False)
    StoreID = db.Column(db.Integer, db.ForeignKey('stores.StoreID'), nullable=False)
    SKUID = db.Column(db.Integer, db.ForeignKey('skus.SKUID'), nullable=False)
    EntryTime = db.Column(db.DateTime, default=datetime.utcnow)
    ExitTime = db.Column(db.DateTime, nullable=True)
    LoadingTime = db.Column(db.DateTime, nullable=True)

    # Relationships
    truck = db.relationship('Truck', backref='assignments')
    store = db.relationship('Store', backref='assignments')
    sku = db.relationship('SKU', backref='assignments')

# Initialize Database
with app.app_context():
    db.create_all()
