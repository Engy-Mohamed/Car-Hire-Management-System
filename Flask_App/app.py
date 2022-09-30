import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS,cross_origin
from getpass import getpass
import random
from flaskext.mysql import MySQL


def setup_db(app):
    try:
        
        #Set database credentials in config.
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql123'
        app.config['MYSQL_DATABASE_DB'] = 'mydb'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'

        #Initialize the MySQL extension
        mysql.init_app(app)
    except Exception as e:
        # 500:(internal service error')Error handlers will handle it 
        abort(500)
        
#Create an instance of MySQL
mysql = MySQL()
app = Flask(__name__)
setup_db(app)
CORS(app)






'''
Use the after_request decorator to set Access-Control-Allow
'''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

  


@app.route('/customers',methods =['POST'])
def add_customer():
    body = request.get_json()
    if body is None:
        abort (400)
    if 'ssn' not in body:
        abort(400)
    

    f_name =body.get('f_name',None)
    l_name =body.get('l_name',None)
    ssn =body.get('ssn',None)
    phone_no =body.get('phone_no',None)
    E_mail =body.get('E_mail',None)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_customer = """INSERT INTO customers(f_name,l_name,ssn, phone_no, E_mail) 
                                VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(insert_customer, (f_name,l_name,ssn, phone_no, E_mail))
        conn.commit()
        response = jsonify(message='customer added successfully.', id=cursor.lastrowid)
        response.status_code = 200
         
    except Exception as e:
        response = jsonify('Failed to add customer.')         
        response.status_code = 400 
    finally:
        cursor.close()
        conn.close()
        return(response)   
     

@app.route('/customers/<int:customer_id>',methods=['PUT'])
def update_customer(customer_id):
    body = request.get_json()
    if body is None:
        abort(400)
    if 'ssn' not in body:
        abort(400)
    f_name =body.get('f_name',None)
    l_name =body.get('l_name',None)
    ssn =body.get('ssn',None)
    phone_no =body.get('phone_no',None)
    E_mail =body.get('E_mail',None)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
      
        update_user_cmd = """update customers 
                                 set f_name=%s, l_name=%s, ssn=%s, phone_no=%s, E_mail=%s
                                 where customer_id=%s"""
        cursor.execute(update_user_cmd, (f_name,l_name,ssn, phone_no, E_mail,customer_id))
        conn.commit()
        response = jsonify(message='customer updated successfully.', id=cursor.lastrowid)
        response.status_code = 200
         
    except Exception as e:
        response = jsonify('Failed to update customer.')         
        response.status_code = 400 
    finally:
        cursor.close()
        conn.close()
        return(response)   
  
@app.route('/customers/<int:customer_id>',methods=['DELETE'])
def delete_customer(customer_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select customer_id from customers where customer_id = %s',customer_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            abort(404)      
        cursor.execute('delete from customers where customer_id = %s',customer_id)
        conn.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        response = jsonify('Failed to delete user.')         
        response.status_code = 400
    finally:
        cursor.close()
        conn.close()    
        return(response)
          
@app.route('/customers/<int:customer_id>')
def get_customer(customer_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from customers where customer_id = %s',customer_id)
        rows = cursor.fetchall()
        if len(rows) == 0:
            abort(404)    
        else:
            response =  jsonify(rows)
    except Exception as e:
        response = jsonify('the customer is not found.')         
        response.status_code = 404 
    finally:
        cursor.close()
        conn.close()
        return response
         
  
'''
   error handlers for all expected errors 
  including 404 and 422. 
'''
@app.errorhandler(404)
def not_found(error):
      return jsonify({
           'success':False,
            'error':404,
            'message':'customer not found' }),404

@app.errorhandler(422)
def unprocessable(error):
      return jsonify({
           'success':False,
            'error':422,
            'message':'unprocessable' }),422

@app.errorhandler(405)
def method_not_allowed(error):
      return jsonify({
           'success':False,
            'error':405,
            'message':'method not allowed' }),405

@app.errorhandler(400)
def bad_request(error):
      return jsonify({
           'success':False,
            'error':400,
            'message':'bad request' }),400

@app.errorhandler(500)
def internal_service_error(error):
      return jsonify({
           'success':False,
            'error':500,
            'message':'internal service error' }),500


    