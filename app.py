from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, SECRET_KEY

app = Flask(__name__)
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.secret_key = SECRET_KEY

mysql = MySQL(app)

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

def store_driver_registration_data(name, gender, dob, license, vehicle_type, vehicle_model, vehicle_classification, license_plate_number,
                                  organization, start_date, route_number):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO drivers (name, gender, dob, license, vehicle_type, vehicle_model, vehicle_classification, license_plate_number, "
        "organization, start_date, route_number, routes) "  # Added 'routes' column
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)",  # Set initial value to NULL
        (name, gender, dob, license, vehicle_type, vehicle_model, vehicle_classification, license_plate_number, organization,
         start_date, route_number)
    )
    mysql.connection.commit()
    cursor.close()

def calculate_working_hours(clock_in_time, clock_out_time):
    # Calculate the working hours based on the clock in/out times
    # You can use any desired method or library for the calculation
    # For example, you can use the datetime module to calculate the time difference
    # and format it accordingly
    clock_in = datetime.strptime(clock_in_time, "%Y-%m-%d %H:%M:%S")
    clock_out = datetime.strptime(clock_out_time, "%Y-%m-%d %H:%M:%S")

    working_hours = clock_out - clock_in
    return str(working_hours)

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
        cursor.close()

        if request.method == 'POST':
            driver_id = request.form.get('driver_id')
            if driver_id:
                cursor = mysql.connection.cursor()
                cursor.execute("DELETE FROM drivers WHERE id = %s", (driver_id,))
                mysql.connection.commit()
                cursor.close()
                flash('Driver data deleted successfully!')

        return render_template('admin.html', drivers=drivers)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        license = request.form.get('license')
        vehicle_type = request.form.get('vehicle_type')
        vehicle_model = request.form.get('vehicle_model')
        vehicle_classification = request.form.get('vehicle_classification')
        license_plate_number = request.form.get('license_plate_number')
        organization = request.form.get('organization')
        start_date = request.form.get('start_date')
        source = request.form.get('source')  # Corrected variable name
        destination = request.form.get('destination')

        name_min_length = 3
        if name is None:
            flash('Name is required.')
            return redirect('/register')

        if len(name) < name_min_length:
            flash(f'Name should have at least {name_min_length} characters.')
            return redirect('/register')

        # Query the database to fetch the route number based on the selected source and destination
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT route_number FROM routes WHERE origin = %s AND destination = %s", (source, destination))
        route = cursor.fetchone()
        cursor.close()

        if not route:
            flash('No matching route found for the selected origin and destination.')
            return redirect('/register')

        route_number = route[0]

        store_driver_registration_data(name, gender, dob, license, vehicle_type, vehicle_model, vehicle_classification, license_plate_number,
                                       organization, start_date, route_number)

        flash('Registration Successful!')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/edit_driver', methods=['GET', 'POST'])
@app.route('/edit_driver/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id=None):
    if request.method == 'POST':
        # Retrieve the updated values from the form
        driver_id = request.form['driver_id']
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        license = request.form['license']
        vehicle_type = request.form['vehicle_type']
        vehicle_model = request.form['vehicle_model']
        vehicle_classification = request.form['vehicle_classification']
        license_plate_number = request.form['license_plate_number']
        organization = request.form['organization']
        start_date = request.form['start_date']
        routes = request.form['routes']

        # Update the corresponding driver in the MySQL table
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE drivers SET Name = %s, Gender = %s, DateOfBirth = %s, DriversLicenseNumber = %s, VehicleType = %s, VehicleModel = %s, VehicleClassification = %s, LicensePlateNumber = %s, Organization = %s, DateStartedInOrganization = %s, RouteNumber = %s WHERE id = %s",
            (name, gender, dob, license, vehicle_type, vehicle_model, vehicle_classification, license_plate_number,
             organization, start_date, routes, driver_id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('edit_driver', driver_id=driver_id))

    else:
        if driver_id:
            # Fetch the specific driver from the MySQL table
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM drivers WHERE id = %s", (driver_id,))
            driver = cursor.fetchone()
            cursor.close()

            if driver:
                return render_template('edit_driver.html', driver=driver)
            else:
                return "Driver not found"

        else:
            # Fetch all drivers from the MySQL table
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM drivers")
            drivers = cursor.fetchall()
            cursor.close()

            return render_template('edit_driver.html', drivers=drivers)
        
@app.route('/edit_driver', methods=['POST'])
def post_edit_driver():
    driver_id = request.form['driver_id']
    return redirect(url_for('edit_driver', driver_id=driver_id))

@app.route('/clock_in_out', methods=['POST'])
def clock_in_out():
    driver_id = request.form.get('driver_id')
    action = request.form.get('action')  # 'clock_in' or 'clock_out'

    # Retrieve the driver from the database using the driver_id
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM drivers WHERE id = %s", (driver_id,))
    driver = cursor.fetchone()
    cursor.close()

    if not driver:
        flash('Invalid driver ID')
        return redirect(url_for('admin'))
    if action not in ['clock_in', 'clock_out']:
        flash('Invalid action!', 'danger')
        return redirect(url_for('home'))

    if action == 'clock_in':
        # Perform clock in operation for the driver
        clock_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock_in_status = 'clocked in'

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE drivers SET clock_in_status = %s, clock_in_time = %s WHERE id = %s",
                       (clock_in_status, clock_in_time, driver_id))
        mysql.connection.commit()
        cursor.close()

        flash('Clock in successful!')
    elif action == 'clock_out':
        # Perform clock out operation for the driver
        clock_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clock_out_status = 'clocked out'

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE drivers SET clock_out_status = %s, clock_out_time = %s WHERE id = %s",
                       (clock_out_status, clock_out_time, driver_id))
        mysql.connection.commit()
        cursor.close()

        # Calculate the working hours for the driver
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT clock_in_time FROM drivers WHERE id = %s", (driver_id,))
        clock_in_time = cursor.fetchone()[0]
        cursor.close()

        working_hours = calculate_working_hours(clock_in_time, clock_out_time)

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE drivers SET working_hours = %s WHERE id = %s", (working_hours, driver_id))
        mysql.connection.commit()
        cursor.close()

        flash('Clock out successful!')
    else:
        flash('Invalid action')

    return redirect(url_for('admin'))


@app.route('/assign_route', methods=['POST'])
def assign_route():
    if 'username' in session and session['role'] == 'admin':
        driver_id = request.form.get('driver_id')
        route = request.form.get('route')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM drivers WHERE id = %s", (driver_id,))
        driver = cursor.fetchone()
        cursor.close()

        if not driver:
            flash('Invalid driver ID')
            return redirect(url_for('admin'))

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE drivers SET route = %s WHERE id = %s", (route, driver_id))
        mysql.connection.commit()
        cursor.close()

        flash('Route assigned successfully!')
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))


@app.route('/remove_route', methods=['POST'])
def remove_route():
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
        cursor.execute("UPDATE drivers SET route = NULL WHERE id = %s", (driver_id,))
        mysql.connection.commit()
        cursor.close()

        flash('Route removed successfully!')
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)