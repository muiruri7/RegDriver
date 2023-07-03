from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from functools import wraps
import sqlite3
import os
import mysql.connector
from werkzeug.utils import secure_filename
import pandas as pd
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB,UPLOAD_FOLDER, SECRET_KEY

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY

mysql = MySQL(app)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Defines!
def retrieve_admin(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND role = 'admin'", (username,))
    admin = cursor.fetchone()
    cursor.close()
    if admin:
        return admin
    else:
        return None

def login(username, password):
    admin = retrieve_admin(username)
    if admin and password == admin[2]:  # Compare the entered password with admin[2]
        return "Login successful"
    else:
        return "Login failed"

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function

def store_driver_registration_data(name, gender, mobile_number, license, national_id, license_plate_number, organization, vehicle_classification, vehicle_model, route_number=None):
    # Set default value for route_number if it is None or empty
    if not route_number:
        route_number = 'N/A'

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO drivers (name, gender, mobile_number, license, national_id, license_plate_number, "
        "organization, vehicle_classification, vehicle_ model, route_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, gender, mobile_number, license,
         national_id, license_plate_number, organization, vehicle_classification, vehicle_model, route_number))

    mysql.connection.commit()
    cursor.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_vehicle(org_name, license_plate, vehicle_type, vehicle_model, vehicle_classification, route_number, driver_status):
    insert_query = f'''
        INSERT INTO {org_name} (
            license_plate_number,
            vehicle_type,
            vehicle_model,
            vehicle_classification,
            route_number,
            driver_status
        ) VALUES (
            '{license_plate}',
            '{vehicle_type}',
            '{vehicle_model}',
            '{vehicle_classification}',
            '{route_number}',
            '{driver_status}'
        )
    '''

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(insert_query)
        mysql.connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error:
        print('Error inserting vehicle:', str(error))
        return False

#Routes!
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = retrieve_admin(username)
        print(admin)  # Print the value of admin for debugging
        if admin and password == admin[1]:  # Compare the entered password with admin[1]
            session['username'] = admin[0]
            session['role'] = admin[2]
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        cursor.execute("SELECT * FROM roster")
        roster = cursor.fetchall()
        driver_id = None
        cursor.close()
        return render_template('admin.html', drivers=drivers, roster=roster, driver_id=driver_id)
    else:
        return redirect(url_for('login'))

@app.route('/delete_driver', methods=['POST'])
def delete_driver():
    if 'username' in session and session['role'] == 'admin':
        driver_id = request.form.get('driver_id')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM drivers WHERE id = %s", (driver_id,))
        driver = cursor.fetchone()
        cursor.close()
        if not driver:
            flash('Invalid driver ID')
            return redirect(url_for('admin'))
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM drivers WHERE id = %s", (driver_id,))
        mysql.connection.commit()
        cursor.close()
        flash('Driver data deleted successfully!')
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        mobile_number = request.form.get('mobile_number')
        license = request.form.get('license')
        national_id = request.form.get('national_id')
        license_plate_number = request.form.get('license_plate_number')
        vehicle_model = request.form.get('vehicle_model')

        # Dictionary mapping table names to organization names
        tables = {
            'super_metro': 'Super Metro',
            'lopha_travellers': 'Lopha Travellers',
            '2nk_sacco': '2NK Sacco',
            'manchester_travellers': 'Manchester Travellers',
            'neo_kenya_mpya_sacco': 'Neo Kenya Mpya Sacco',
            '4nte_sacco': '4NTE Sacco',
            'naekana_sacco': 'Naekana Sacco'
        }

        cursor = mysql.connection.cursor()
        route_number = None

        for table, org_name in tables.items():
            cursor.execute(f"SELECT vehicle_classification,vehicle_model, route_number FROM {table} WHERE license_plate_number = %s", (license_plate_number,))
            result = cursor.fetchone()
            if result:
                organization = org_name
                vehicle_classification = result[0]
                vehicle_model = result[1]
                route_number = result[2]
                break

        if route_number is None:
            flash('License plate number not found')
            return redirect(url_for('home'))

        cursor.execute(
            "INSERT INTO drivers (name, gender, mobile_number, license, national_id, license_plate_number, organization, vehicle_classification, vehicle_model, route_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (name, gender, mobile_number, license, national_id, license_plate_number, organization, vehicle_classification, vehicle_model, route_number))
        
        mysql.connection.commit()

        flash('Driver registration successful')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/getdata')
def getdata():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM drivers")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/edit_driver/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    # Retrieve driver information from the database
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM drivers WHERE id=%s"
    cursor.execute(query, (driver_id,))
    driver = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Get updated driver information from the form
        name = request.form.get('name')
        gender = request.form.get('gender')
        mobile_number = request.form.get('mobile_number')
        license = request.form('license')
        national_id = request.form.get('national_id')
        license_plate_number = request.form('license_plate_number')
        organization = request.form('organization')
        vehicle_classification = request.form(vehicle_classification)
        vehicle_model = request.form('vehicle_model')
        route_number = request.form('route_number')

        # Update driver information in the database
        cursor = mysql.connection.cursor()
        query = "UPDATE drivers SET name=%s, gender=%s, mobile_number=%s, license=%s, national_id=%s, license_plate_number=%s, organization=%s, vehicle_classification=%s, vehicle_model=%s, route_number=%s WHERE id=%s"
        cursor.execute(query, (name, gender, mobile_number, license, national_id, license_plate_number, organization, vehicle_classification, vehicle_model, route_number, driver_id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin'))

    return render_template('edit_driver.html', driver=driver)
        
@app.route('/edit_driver', methods=['POST'])
def post_edit_driver():
    driver_id = request.form['driver_id']
    return redirect(url_for('edit_driver', driver_id=driver_id))

@app.route('/management/<int:driver_id>', methods=['GET', 'POST'])
def management(driver_id):
    # Retrieve driver name from the database
    mycursor = mysql.connection.cursor()
    query = "SELECT name FROM drivers WHERE id=%s"
    mycursor.execute(query, (driver_id,))
    driver_name = mycursor.fetchone()[0]

    if request.method == 'POST':
        name = request.form.get('name')
        clock_in = request.form.get('clock_in')
        clock_out = request.form.get('clock_out')
        pickup_point = request.form.get('pickup_point')
        destination = request.form.get('destination')

        # Retrieve route number from routes table
        sql = "SELECT route_number FROM routes WHERE pickup_point = %s AND destination = %s"
        val = (pickup_point, destination)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        # Insert data into roster table
        if result:
            route_number = result[0]
            sql = "INSERT INTO roster (name, clock_in, clock_out, pickup_point, destination, route_number, driver_status, reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (name, clock_in, clock_out, pickup_point, destination, route_number, driver_status, reason)
            mycursor.execute(sql, val)
            mysql.connection.commit()

            flash('Driver scheduled successfully')
            return redirect(url_for('home'))
        else:
            flash('No route found for the selected pickup point and destination')

    # Retrieve distinct pickup points from routes table
    mycursor.execute("SELECT DISTINCT pickup_point FROM routes")
    pickup_points = mycursor.fetchall()

    # Retrieve distinct destinations from routes table
    mycursor.execute("SELECT DISTINCT destination FROM routes")
    destinations = mycursor.fetchall()

    mycursor.close()

    return render_template('management.html', driver_name=driver_name, pickup_points=pickup_points, destinations=destinations)

@app.route('/organizations', methods=['GET', 'POST'])
def organizations():
    if request.method == 'POST':
        org_name = request.form.get('org_name')

        if org_name is None:
            return "Missing 'org_name' field", 400

        create_table_query = f'''
            CREATE TABLE {org_name} (
                license_plate_number VARCHAR(20),
                vehicle_model VARCHAR(50),
                vehicle_classification VARCHAR(50),
                route_number INT(20),
                vehicle_status ENUM('suspended', 'engaged')
            )
        '''

        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute(create_table_query)
            mysql.connection.commit()
            return 'Organization registered successfully.'
        except mysql.connector.Error as error:
            return 'Error registering organization: {}'.format(error)
    else:
        return render_template('organizations.html')

@app.route('/vehicles', methods=['GET'])
def render_vehicles():
    return render_template('vehicles.html')

@app.route('/upload_spreadsheet', methods=['POST'])
def upload_spreadsheet():
    # Check if file was uploaded
    if 'spreadsheet' not in request.files:
        return "No spreadsheet file provided", 400

    file = request.files['spreadsheet']

    # Check if file has a valid filename and extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the uploaded file
        file.save(file_path)

        try:
            # Read data from the spreadsheet using pandas
            df = pd.read_excel(file_path)

            # Process and insert the data into the database
            for index, row in df.iterrows():
                license_plate_number = row['License Plate Number']
                vehicle_type = row['Vehicle Type']
                vehicle_model = row['Vehicle Model']
                vehicle_classification = row['Vehicle Classification']
                route_number = row['Route Number']
                driver_status = row['Driver Status']

                # Perform database insertion
                success = insert_vehicle( license_plate_number, vehicle_type, vehicle_model, vehicle_classification, route_number, driver_status)

                if not success:
                    return 'Error inserting vehicles', 500

            return 'Vehicles added successfully.'
        except Exception as e:
            return 'Error processing spreadsheet: {}'.format(str(e)), 500
    else:
        return 'Invalid spreadsheet file', 400

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)