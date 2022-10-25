from flask import Flask, redirect, url_for, request, render_template
import psycopg2
from datetime import datetime

app = Flask(__name__)

db_connect = psycopg2.connect(
    host="10.17.10.70",
    database="group_9",
    user="group_9",
    password="6xKbIOpFFobZr",
    port="5432"
)
db_connect.autocommit = True

cust_id = 0
def get_avail_flights():
    return "select airlines.AIRLINE, FLIGHT_NUMBER, ORIGIN_AIRPORT, DESTINATION_AIRPORT, YEAR, MONTH, DAY,SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL from airlines, flights where airlines.IATA_CODE = flights.AIRLINE AND flights.origin_airport = '%s' AND flights.destination_airport = '%s' AND MONTH = %s AND DAY = %s"

def get_avail_airline():
    return "select airlines.AIRLINE, FLIGHT_NUMBER, ORIGIN_AIRPORT, DESTINATION_AIRPORT, YEAR, MONTH, DAY,SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL from airlines, flights where airlines.IATA_CODE = flights.AIRLINE AND flights.origin_airport = '%s' AND flights.destination_airport = '%s' AND MONTH = %s AND DAY = %s AND airlines.AIRLINE = '%s'"

def ent_user_info():
    return "INSERT INTO customer_info VALUES (%s, '%s' , '%s', '%s', '%s', '%s', '%s', %s, %s)"

def num_of_cust():
    return "SELECT COUNT(cust_id) FROM customer_info"

def get_cust():
    return "SELECT cust_id, cust_name, cust_age, cust_dob, cust_phone, cust_email, cust_pass, cust_flight FROM customer_info WHERE cust_id='%s'"

def update_user_info():
    return "UPDATE customer_info SET cust_age = '%s', cust_dob = '%s', cust_phone = '%s', cust_email = '%s', cust_pass = '%s' WHERE cust_id = '%s'"

def get_fs():
    return "SELECT airline, scheduled_departure, departure_time, departure_delay, diverted, cancelled FROM flights WHERE month = '%s' AND day = '%s' AND flight_number = '%s' AND origin_airport='%s' AND destination_airport='%s'"

def indirect_flights():
    return "select table1.firstoa, table1.firstda, table1.secondoa, table1.secondda, table1.firstfn, table1.secondfn, table1.YEAR, table1.MONTH, table1.DAY, airlines.airline, table1.firstsd, table1.firstsa, table1.secondsd, table1.secondsa from airlines,(select a.ORIGIN_AIRPORT as firstoa , a.DESTINATION_AIRPORT as firstda, b.ORIGIN_AIRPORT as secondoa, b.DESTINATION_AIRPORT as secondda,a.FLIGHT_NUMBER as firstfn, b.FLIGHT_NUMBER as secondfn, a.YEAR, a.MONTH, a.DAY,  a.AIRLINE as airline, a.SCHEDULED_DEPARTURE as firstsd, a.SCHEDULED_ARRIVAL as firstsa, b.SCHEDULED_DEPARTURE as secondsd, b.SCHEDULED_ARRIVAL as secondsa   from flights as  a , flights as b  where a.destination_airport = b.origin_airport and  a.destination_airport <> '%s' and a.YEAR = 2015 AND a.MONTH = %s AND a.DAY = %s and b.YEAR = 2015 AND b.MONTH = %s AND b.DAY = %s and a.AIRLINE=b.AIRLINE and a.origin_airport = '%s' and b.destination_airport = '%s' and a.SCHEDULED_ARRIVAL < b.SCHEDULED_DEPARTURE and a.SCHEDULED_DEPARTURE < b.SCHEDULED_DEPARTURE and a.SCHEDULED_ARRIVAL < b.SCHEDULED_ARRIVAL) as table1 where airlines.IATA_CODE = table1.AIRLINE"

def add_flight():
    return "INSERT INTO flights (YEAR, MONTH, DAY, AIRLINE, FLIGHT_NUMBER, ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, DEPARTURE_TIME, DEPARTURE_DELAY, SCHEDULED_TIME, DISTANCE, SCHEDULED_ARRIVAL, DIVERTED, CANCELLED) VALUES (%s, %s, %s, '%s', %s, '%s', '%s', %s, %s, 0, %s, %s, %s, 0, 0)"

def add_airport():
    return "INSERT INTO airports (IATA_CODE, AIRPORT, CITY, STATE, COUNTRY) VALUES ('%s', '%s', '%s', '%s', '%s')"

def add_airline():
    return "INSERT INTO airlines (IATA_CODE, AIRLINE) VALUES ('%s', '%s')"

def update_flight():
    return "UPDATE flights SET DEPARTURE_TIME = %s, DEPARTURE_DELAY = %s, SCHEDULED_TIME = %s, SCHEDULED_ARRIVAL = %s, DIVERTED = %s, CANCELLED = %s WHERE MONTH = %s AND DAY = %s AND FLIGHT_NUMBER = %s AND ORIGIN_AIRPORT = '%s' AND  DESTINATION_AIRPORT = '%s'"

def cities_flights():
    return "select airlines.AIRLINE,table1.FLIGHT_NUMBER, table1.ORIGIN_AIRPORT, table1.DESTINATION_AIRPORT, table1.YEAR, table1.MONTH, table1.DAY, table1.SCHEDULED_DEPARTURE, table1.SCHEDULED_ARRIVAL from airlines, (select flights.AIRLINE as AIRLINE, FLIGHT_NUMBER, ORIGIN_AIRPORT, DESTINATION_AIRPORT, YEAR, MONTH, DAY, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL from flights, airports as a1, airports as a2 where a1.IATA_CODE = flights.ORIGIN_AIRPORT AND a2.IATA_CODE = flights.DESTINATION_AIRPORT AND a1.city = '%s' AND a2.city = '%s' AND MONTH = %s AND DAY = %s) as table1 where airlines.IATA_CODE = table1.AIRLINE"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/ticketbooking')
def ticketbooking():
    return render_template('ticket booking.html')

@app.route('/flightstatus')
def flightstatus():
    return render_template('flight status.html')

@app.route('/updatedetails')
def updatedetails():
    return render_template('update details.html')

@app.route('/adminaccess')
def adminaccess():
    return render_template('admin access.html')

@app.route('/searchflights')
def searchflights():
    return render_template('search flights.html')

@app.route('/searchcities')
def searchcities():
    return render_template('search cities.html')

@app.route('/findflights', methods=['POST','GET'])
def findflights():
    if request.method == 'POST':
        orig = request.form['origin_airport']
        des = request.form['dest_airport']
        date = request.form['date_of_travel']
        my_date = datetime.strptime(date, "%Y-%m-%d")
        day = my_date.day
        month = my_date.month
        year = my_date.year
        cur = db_connect.cursor()
        cur.execute(get_avail_flights() %(orig,des, month, day))
        rows = cur.fetchall()
        cur.close()
        return render_template('available flights.html', result=rows)

@app.route('/findflightscities', methods=['POST','GET'])
def findflightscities():
    if request.method == 'POST':
        orig = request.form['origin_city']
        des = request.form['dest_city']
        date = request.form['date_of_travel']
        my_date = datetime.strptime(date, "%Y-%m-%d")
        day = my_date.day
        month = my_date.month
        year = my_date.year
        cur = db_connect.cursor()
        cur.execute(cities_flights() %(orig,des, month, day))
        rows = cur.fetchall()
        cur.close()
        return render_template('available flights.html', result=rows)


@app.route('/findairline/<orig>/<des>/<month>/<day>', methods=['POST', 'GET'])
def findairline(orig,des,month,day):
    airline = request.form['airline']
    cur = db_connect.cursor()
    cur.execute(get_avail_airline() %(orig,des, month, day, airline))
    rows = cur.fetchall()
    cur.close()
    return render_template('available flights.html', result = rows)

@app.route('/user_details/<flight>', methods=['POST','GET'])
def user_details(flight):
    return render_template('user details.html', flight = flight)

@app.route('/user_info/<flight>', methods=['POST','GET'])
def user_info(flight):
    user_name = request.form['user_name']
    user_age = request.form['user_Age']
    user_dob = request.form['user_dob']
    user_phone = request.form['user_phone']
    user_email = request.form['user_email']
    user_pass = request.form['user_pass']
    cur = db_connect.cursor()
    cur.execute(num_of_cust())
    cust_id_str = cur.fetchall()
    cust_id = int(cust_id_str[0][0])
    cur.execute(ent_user_info() %((cust_id +1), user_name, user_age, str(user_dob), user_phone, user_email, user_pass, flight, 1))
    cur.close()
    return render_template('ticket.html', flight_id = flight, cust_id = cust_id, cust_name = user_name, cust_age = user_age, cust_dob = user_dob, cust_phone = user_phone, cust_email = user_email, cust_pass= user_pass)

@app.route('/usernewdetails', methods=['POST','GET'])
def usernewdetails():
    cust_id = request.form['cust_id']
    cur = db_connect.cursor()
    cur.execute(get_cust() % cust_id)
    cust_details = cur.fetchall()
    return render_template('user new details.html', user_dt = cust_details[0])

@app.route('/user_new_info/<cust_id>/<cust_name>/<flight_id>', methods=['POST', 'GET'])
def user_new_info(cust_id, cust_name, flight_id):
    user_age = request.form['user_age']
    user_dob = request.form['user_dob']
    user_phone = request.form['user_phone']
    user_email = request.form['user_email']
    user_pass = request.form['user_pass']
    cur = db_connect.cursor()
    cur.execute(update_user_info() %(user_age, str(user_dob), user_phone, user_email, user_pass, cust_id))
    cur.close()
    return render_template('ticket.html', flight_id = flight_id, cust_id = cust_id, cust_name = cust_name, cust_age = user_age, cust_dob = user_dob, cust_phone = user_phone, cust_email = user_email, cust_pass= user_pass)

@app.route('/flight_status', methods=['POST','GET'])
def flight_status():
    origin = request.form['origin_airport']
    dest = request.form['dest_airport']
    flight_id = request.form['flight_id']
    date = request.form['date_of_travel']
    my_date = datetime.strptime(date, "%Y-%m-%d")
    day = my_date.day
    month = my_date.month
    cur = db_connect.cursor()
    cur.execute(get_fs() %(month, day, flight_id, origin, dest))
    result = cur.fetchall()
    res = result[0]
    delay = res[3]
    if delay<0:
        str = "ADVANCED"
    elif delay==0:
        str = "ON TIME"
    else: 
        str = "DELAYED"
    divert = res[4]
    if divert ==1: str = "DIVERTED"
    cancel = res[5]
    if cancel ==1: str = "CANCELED"
    cur.close()
    return render_template('fs result.html', result = res, origin = origin, dest=dest, date = date, flight_id = flight_id, status=str)

@app.route('/addflight')
def addflight():
    return render_template('add flight.html')

@app.route('/addflightdetails', methods=['POST', 'GET'])
def addflightdetails():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    airline = request.form['airline']
    flightnum = request.form['flight_number']
    orig = request.form['origin_airport']
    des = request.form['destination_airport']
    dept = request.form['scheduled_departure']
    time = request.form['scheduled_time']
    distance = request.form['distance']
    arrival = request.form['scheduled_arrival']
    cur = db_connect.cursor()
    cur.execute(add_flight() %(year, month, day, airline, flightnum, orig, des, dept, dept, time, distance, arrival))
    cur.close()
    return render_template('success.html', result = "FLIGHT", ans = 1)

@app.route('/addairport', methods=['POST', 'GET'])
def addairport():
    return render_template('add airport.html')

@app.route('/addairportdetails', methods=['POST', 'GET'])
def addairportdetails():
    iata = request.form['iata_code']
    airport = request.form['airport']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    cur = db_connect.cursor()
    cur.execute(add_airport() %(iata, airport, city, state, country))
    cur.close()
    return render_template('success.html', result = "AIRPORT", ans = 1)

@app.route('/addairline', methods=['POST', 'GET'])
def addairline():
    return render_template('add airline.html')

@app.route('/addairlinedetails', methods=['POST', 'GET'])
def addairlinedetails():
    iata = request.form['iata_code']
    airline = request.form['airline']
    cur = db_connect.cursor()
    cur.execute(add_airline() %(iata, airline))
    cur.close()
    return render_template('success.html', result = "AIRLINE", ans = 1)

@app.route('/updateflight', methods=['POST','GET'])
def updateflight():
    return render_template('flight details.html')

@app.route('/flightnewdetails', methods=['POST','GET'])
def flightnewupdates():
    orig = request.form['origin_airport']
    des = request.form['dest_airport']
    date = request.form['date_of_travel']
    flight = request.form['flight_id']
    my_date = datetime.strptime(date, "%Y-%m-%d")
    day = my_date.day
    month = my_date.month
    year = my_date.year
    cur = db_connect.cursor()
    cur.execute(get_avail_flights() %(orig,des, month, day))
    rows = cur.fetchall()
    cur.close()
    return render_template('new flight updates.html', orig = orig, des = des, day = day, month = month, flight = flight)

@app.route('/flightupdatedetails/<orig>/<dest>/<day>/<month>/<flight>', methods=['POST','GET'])
def flightupdatedetails(orig, dest, day, month, flight):
    dept_time = request.form['updated dept time']
    dept_delay = request.form['departure delay']
    arrival = request.form['updated arrival time']
    schd_time = request.form['updated schd time']
    divert = request.form['diverted']
    cancel = request.form['cancelled']
    cur = db_connect.cursor()
    cur.execute(update_flight() %(dept_time, dept_delay, arrival, schd_time, divert, cancel, month, day, flight, orig, dest))
    cur.close()
    return render_template('success.html', result = "AIRLINE", ans = 0)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5009",debug=True)

db_connect.close()