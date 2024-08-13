from flask import request, jsonify, current_app as app
from flask_restful import Resource
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def connect():
    conn = sqlite3.connect('warehouse.db')
    return conn

class UserAPI(Resource):
    def get(self):
        data = request.get_json()
        employeeid = data.get('employeeid')
        password = data.get('password')
        
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM Users WHERE EmployeeID=? AND Password=?', (employeeid, password)).fetchone()
        conn.close()
        
        if fetch:
            return {'message': 'Login Successful', 'role': fetch[2]}, 200
        else:
            return {'message': 'Invalid Credentials'}, 401

    def post(self):
        data = request.get_json()
        employeeid = data.get('employeeid')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role')
        
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM Users WHERE EmployeeID=?', (employeeid,)).fetchall()
        
        if fetch:
            conn.close()
            return {'message': 'User already registered'}, 400
        else:
            cursor.execute('INSERT INTO Users (EmployeeID, Name, Role, Password) VALUES (?, ?, ?, ?)', (employeeid, name, role, password))
            conn.commit()
            conn.close()
            return {'message': 'Registration successful'}, 200

        

class TruckAPI(Resource):
    def get(self, TruckID):
        data = request.get_json()
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM trucks WHERE TruckID = ?', (TruckID,)).fetchone()
        conn.close()

        if fetch:
            trucks = {
                'TruckID': fetch[0],
                'Truck Number Plate': fetch[1],
                'Driver Name': fetch[2],
                'Driver License ID': fetch[3],
                'Driver Contact': fetch[4],
                'Truck RFID': fetch[5]
            }
            return {'trucks': trucks}, 200
        else:
            return {'message': 'No trucks found'}, 404
    
    def post(self,TruckID):
        data = request.get_json()
        
        truck_number_plate = data.get('truck_number_plate')
        driver_name = data.get('driver_name')
        driver_license_id = data.get('driver_license_id')
        driver_contact = data.get('driver_contact')
        truck_rfid = data.get('truck_rfid')
        
        conn = connect()
        cursor = conn.cursor()
            
        if not all([truck_number_plate, driver_name, driver_license_id, driver_contact, truck_rfid]):
            return {'message': 'Data unavailable: All fields are required.'}, 400
        
        fetch = cursor.execute('SELECT * FROM trucks WHERE TruckID = ?', (TruckID,)).fetchall()
    
        if fetch:
            conn.close()
            return {'message': 'Truck with this ID already registered'}, 400
        else:
            cursor.execute('INSERT INTO trucks (TruckNumberPlate, DriverName, DriverLicenseID, DriverContact, TruckRFID) VALUES (?, ?, ?, ?, ?)', 
                           (truck_number_plate, driver_name, driver_license_id, driver_contact, truck_rfid))
        
        conn.commit()
        conn.close()
        return {'message': 'Truck added successfully'}, 200
    
    def delete(self):
        data = request.get_json()
        truck_id = data.get('truck_id')
        conn = connect()
        cursor = conn.cursor()
        
        fetch = cursor.execute('SELECT * FROM trucks WHERE TruckID = ?', (truck_id,)).fetchone()
        
        if fetch:
            cursor.execute('DELETE FROM trucks WHERE TruckID = ?', (truck_id,))
            conn.commit()
            conn.close()
            return {'message': 'Truck deleted successfully'}, 200
        else:
            conn.close()
            return {'message': 'Truck not found'}, 404
             
    def put(self):
        data = request.get_json()
        truck_id = data.get('truck_id')
        truck_number_plate = data.get('truck_number_plate')
        driver_name = data.get('driver_name')
        driver_license_id = data.get('driver_license_id')
        driver_contact = data.get('driver_contact')
        truck_rfid = data.get('truck_rfid')
        
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM trucks WHERE TruckID = ?', (truck_id,)).fetchone()
        if fetch:
            cursor.execute('UPDATE trucks SET TruckNumberPlate = ?, DriverName = ?, DriverLicenseID = ?, DriverContact = ?, TruckRFID = ? WHERE TruckID = ?', 
                           (truck_number_plate, driver_name, driver_license_id, driver_contact, truck_rfid, truck_id))
            conn.commit()
            conn.close()
            return {'message': 'Truck details updated successfully'}, 200
        else:
            conn.close()
            return {'message': 'Truck not found'}, 404
        
        
class StoreAPI(Resource):
    def get(self):
        data = request.get_json()
        store_id = data.get('store_id')
        conn = connect()  
        cursor = conn.cursor()

        if store_id:
            
            fetch = cursor.execute('SELECT * FROM stores WHERE StoreID=?', (store_id,)).fetchone()
            conn.close()

            if fetch:
                store = {
                    'StoreID': fetch[0],
                    'Store Name': fetch[1],
                    'Store Manager': fetch[2],
                    'Store Contact': fetch[3],
                    'Store Address': fetch[4]
                }
                return {'store': store}, 200
            else:
                return {'message': 'Store not found'}, 404

    def post(self,StoreID):
        data = request.get_json()
        
        store_name = data.get('store_name')
        store_manager = data.get('store_manager')
        store_contact = data.get('store_contact')
        store_address = data.get('store_address')
        
        # Check if any required field is missing or empty
        if not all([store_name, store_manager, store_contact, store_address]):
            return {'message': 'Data unavailable: All fields are required.'}, 400
        
        conn = connect()
        cursor = conn.cursor()

        # Check if a store with the same name already exists
        fetch = cursor.execute('SELECT * FROM stores WHERE StoreID =?', (StoreID)).fetchall()
        
        if fetch:
            conn.close()
            return {'message': 'Store with this name already registered'}, 400
        else:
            cursor.execute('INSERT INTO stores (Store Name, Store Manager, Store Contact, Store Address) VALUES (?, ?, ?, ?)', 
                           (store_name, store_manager, store_contact, store_address))
            conn.commit()
            conn.close()
            return {'message': 'Store added successfully'}, 200
        
    def delete(self):
        data = request.get_json()
        store_id = data.get('store_id')
        conn = connect()
        cursor = conn.cursor()
        
        fetch = cursor.execute('SELECT * FROM stores WHERE StoreID=?', (store_id,)).fetchone()
        if fetch:
            cursor.exicute('DELETE FROM stores WHERE StoreID =?',(store_id,))
            conn.commit()
            conn.close()
            return{'message':'Store deleted'},200
        else:
            conn.close()
            return{'message':'Store does not exist'},404
    
    
    def put(self):
        data = request.get_json()
        store_id = data.get('store_id')
        store_name = data.get('store_name')
        store_manager = data.get('store_manager')
        store_contact = data.get('store_contact')
        store_address = data.get('store_address')
        
        
        if not all([store_id, store_name, store_manager, store_contact, store_address]):
            return {'message': 'Data unavailable: All fields are required.'}, 400
        
        conn = connect()
        cursor = conn.cursor()

        # Check if the store with the given ID exists
        fetch = cursor.execute('SELECT * FROM stores WHERE StoreID=?', (store_id,)).fetchone()
        
        if fetch:
            cursor.execute('UPDATE stores SET Store Name=?, Store Manager=?, Store Contact=?, Store Address=? WHERE StoreID=?', 
                           (store_name, store_manager, store_contact, store_address, store_id))
            conn.commit()
            conn.close()
            return {'message': 'Store details updated successfully'}, 200
        else:
            conn.close()
            return {'message': 'Store not found '}, 404
            
            
class SKUAPI(Resource):
    def get(self):
        data = request.get_json()
        sku_id = data.get('sku_id')
        conn = connect()
        cursor = conn.cursor()

        
        fetch = cursor.execute('SELECT * FROM sku WHERE SKUID=?', (sku_id,)).fetchone()
        conn.close()

        if fetch:
            sku = {
                'SKUID': fetch[0],
                'SKU Name': fetch[1],
                'Warehouse Number': fetch[2]
            }
            return {'sku': sku}, 200
        else:
            return {'message': 'SKU not found'}, 404
        
        

    def post(self,SKUID):
        data = request.get_json()
        
        sku_name  = data.get('sku_name')
        warehouse_number = data.get('warehouse_number')

        if not all([sku_name, warehouse_number]):
            return {'message': 'Data unavailable: SKU Name and Warehouse Number are required.'}, 400

        conn = connect()
        cursor = conn.cursor()

    
        fetch = cursor.execute('SELECT * FROM sku WHERE SKUID=?', (SKUID)).fetchall()

        if fetch:
            conn.close()
            return {'message': 'SKU with this name already exists'}, 400
        else:
            cursor.execute('INSERT INTO sku (SKU Name, Warehouse Number) VALUES (?, ?)', 
                           (sku_name, warehouse_number))
            conn.commit()
            conn.close()
            return {'message': 'SKU added successfully'}, 201
        
    def delete(self):
        data = request.get_json  
        sku_id = data.get('sku_id')

        conn = connect()
        cursor = conn.cursor()

        fetch = cursor.execute('SELECT * FROM sku WHERE SKUID=?', (sku_id,)).fetchone()

        if fetch:
            cursor.execute('DELETE FROM sku WHERE SKUID=?', (sku_id,))
            conn.commit()
            conn.close()
            return {'message': 'SKU deleted successfully'}, 200
        else:
            conn.close()
            return {'message': 'SKU not found'}, 404
        
    
    def put(self):
        data = request.get_json()
        sku_id = data.get('sku_id')
        sku_name = data.get('sku_name')
        warehouse_number = data.get('warehouse_number')

        if not all([sku_id, sku_name, warehouse_number]):
            return {'message': 'Data unavailable: All fields are required.'}, 400

        conn = connect()
        cursor = conn.cursor()

        
        fetch = cursor.execute('SELECT * FROM sku WHERE SKUID=?', (sku_id,)).fetchone()

        if fetch:
            cursor.execute('UPDATE sku SET SKU Name=?, Warehouse Number=? WHERE SKUID=?', 
                           (sku_name, warehouse_number, sku_id))
            conn.commit()
            conn.close()
            return {'message': 'SKU details updated successfully'}, 200
        else:
            conn.close()
            return {'message': 'SKU not founded '}, 404
        
        

class AssignmentApi(Resource):
    def get(self):
        data = request.get_json()  
        assignment_id = data.get('assignment_id')
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM assignments WHERE AssignmentID=?', (assignment_id,)).fetchone()
        conn.close()

        if fetch:
            assignment = {
                'Assignment ID': fetch[0],
                'TruckID': fetch[1],
                'StoreID': fetch[2],
                'SKUID': fetch[3],
                'Entry Time': fetch[4],
                'Exit Time': fetch[5],
                'Loading Time': fetch[6]
                }
            return {'assignment': assignment}, 200
        else:
            return {'message': 'Assignment not found'}, 404
        
    def post(self,AssignmentID):
        data = request.get_json()
        
        truck_id = data.get('truck_id')
        store_id = data.get('store_id')
        sku_id = data.get('sku_id')
        entry_time = data.get('entry_time')
        exit_time = data.get('exit_time')
        loading_time = data.get('loading_time')

        if not all([truck_id, store_id, sku_id, entry_time, exit_time, loading_time]):
            return {'message': 'Data unavailable: All fields are required.'}, 400
        
        #current date and time
        current_datetime = datetime.now()

        conn = connect()
        cursor = conn.cursor()
        
        fetch = cursor.execute('SELECT * FROM assignment WHERE Assignment ID = ?',(AssignmentID)).fetchall()
        
        if fetch:
            conn.close()
            return{'message':'Assignment already exist'},404
        else :
            cursor.execute('INSERT INTO assignments (TruckID, StoreID, SKUID, Entry Time, Exit Time, Loading Time) VALUES (?, ?, ?, ?, ?, ?)', 
                       (truck_id, store_id, sku_id, current_datetime, current_datetime, current_datetime))
            conn.commit()
            conn.close()
            return {'message': 'Assignment added successfully'}, 201
        
    def delete(self):
        data = request.get_json()
        assignment_id = data.get('assignment_id')
        conn = connect()
        cursor = conn.cursor()
        
        fetch = cursor.execute('SELECT * FROM assingment WHERE Assignment ID =?',(assignment_id))
        if fetch:
            conn.execute('DELETE * FROM assignment WHERE Assignment ID =?',(assignment_id))
            conn.close()
            conn.commit()
            return{'message':'assignment deleted'}
        else: 
            return{'message':'assignment not found'}
    
    
    def put(self):
        data = request.get_json()
        assignment_id = data.get('assignment_id')
        truck_id = data.get('truck_id')
        store_id = data.get('store_id')
        sku_id = data.get('sku_id')
        entry_time = data.get('entry_time')
        exit_time = data.get('exit_time')
        loading_time = data.get('loading_time')    

        conn = connect()
        cursor = conn.cursor()

        fetch = cursor.execute('SELECT * FROM assignments WHERE AssignmentID=?', (assignment_id,)).fetchone()

        if fetch:
            cursor.execute('''UPDATE assignment SET TruckID=?, StoreID=?,
                           SKUID=?, EntryTime=?, ExitTime =?, LoadingTime=? WHERE AssignmentID=?''',(truck_id, store_id, sku_id, entry_time, exit_time, loading_time,assignment_id))
            conn.commit()
            conn.close()
            return {'message': 'Assignment updated successfully'}, 200
        else:
            conn.close()
            return {'message': 'Assignment not found'}, 404
