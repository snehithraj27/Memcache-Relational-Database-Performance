# Author: Snehith Raj Bada

import io
from flask import Flask, render_template, request
import csv
from datetime import datetime
# Author: Snehith Raj Bada

import sqlite3
import memcache

app = Flask(__name__)
#Connect to SQL Database
con=sqlite3.connect("database.db")
#Home page of the application
cur=con.cursor()
mc = memcache.Client(['127.0.0.1:11211'], debug=1,cache_cas=True);
@app.route('/')
def home():
    return render_template('home.html')

#Method to create table
@app.route('/createtable',methods=['POST', 'GET'])
def create_table():
    if request.method == 'POST':
        start = datetime.now()
        con.execute("CREATE TABLE if not exists earthquake(time varchar(30), latitude float(20), longitude float(20), depth float(10), mag float(10), magType varchar(10), nst int, gap int, dmin float(20), rms float(10),net varchar(10), id varchar(20), updated varchar(30),place varchar(50), type varchar(20),horizontalError float(10), depthError float(10), magError float(10), magNst int, status varchar(20),locationSource varchar(10),magSource varchar(10))")
        time_taken=datetime.now() - start
        con.commit()
        result="Time to create table :{0}".format(time_taken)
        print(result)
        return render_template("result.html",msg=result)

# Method to delete table
@app.route('/deletetable',methods=['POST', 'GET'])
def delete_table():
    if request.method == 'POST':
        start = datetime.now()
        cur.execute("Drop table earthquake")
        time_taken = datetime.now() - start
        con.commit()
        result="Time to delete table :{0}".format(time_taken)
        print(result)
        return render_template("result.html", msg=result)

#Method for reading the uploaded csv file
@app.route('/upload', methods=['POST', 'GET'])
def insert_table():
    if request.method == 'POST':
        f = request.files['data_file']
        if not f:
            return "No file"
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)
        start = datetime.now()
        print(start)
        for row in csv_input:
            cur.execute(
                "INSERT INTO earthquake(time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms,net, id,updated, place,type,horizontalError, depthError, magError, magNst,status, locationSource,magSource) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
            con.commit()
        time_taken = datetime.now() - start
        result="Time to insert records table :{0}".format(time_taken)
        return render_template('result.html',msg=result)

#Method to display all the records
@app.route('/getrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        cur.execute('''SELECT * from earthquake''')
        rv = cur.fetchall()
        return render_template("data.html", msg=rv)

#Method to delete all the records
@app.route('/deleterecords', methods=['POST', 'GET'])
def delete_records():
    if request.method == 'POST':
        cur.execute("delete from earthquake")
        con.commit()
        return render_template("result.html", msg="All records deleted")

# Method to generate random queries
@app.route('/queries', methods=['POST', 'GET'])
def generate_queries():
    if request.method == 'POST':
        number=int(request.form["value"])
        start=datetime.now()
        while(number>0):
            cur.execute("SELECT * FROM earthquake ORDER BY RANDOM()")
            cur.fetchall()
            print(number)
            number=number-1
        time_taken = datetime.now() - start
        print(time_taken)
        return render_template("result.html", msg="Time to generate {0} random queries is {1}".format(number,time_taken))

# Method to generate random random based on magnitude
@app.route('/queriesvalue', methods=['POST', 'GET'])
def generate_queriesvalue():
    if request.method == 'POST':
        number = int(request.form["no"])
        value=int(request.form["value"])
        start=datetime.now()
        while(number>0):
            cur.execute("SELECT * FROM earthquake where mag >? ORDER BY RANDOM()",('{}'.format(value),))
            row=cur.fetchall()
            print(number)
            number=number-1
        time_taken = datetime.now() - start
        print(time_taken)
        return render_template("result.html", msg="Time to generate random queries is {1}".format(number,time_taken))

# Method to generate random queries - Memcache
@app.route('/queriesmemcache', methods=['POST', 'GET'])
def generate_queries_memcahe():
    if request.method == 'POST':
        number = int(request.form["value"])
        start = datetime.now()
        try:
            equake=mc.get('records')
            print(equake)
        except (mc.MemcachedKeyTypeError, mc.MemcachedKeyNoneError,
                TypeError, mc.MemcachedKeyCharacterError,
                mc.MemcachedKeyError, mc.MemcachedKeyLengthError,
                mc.MemcachedStringEncodingError):
            print('error')
        if not equake:
            x='DB'
            while (number > 0):
                cur.execute("SELECT * FROM earthquake ORDER BY RANDOM()")
                rows=cur.fetchall()
                print(rows)
                mc.set('records',rows,time=900)
                print(number)
                number = number - 1
            time_taken = datetime.now() - start
            print(time_taken)
        else:
            time_taken = datetime.now() - start
            x = 'MemCache'
    return render_template("result.html",
                           msg="Time to generate random queries is {0} from {1}".format(time_taken,x))

# Method to generate random random based on magnitude - Memcache
@app.route('/queriesvaluememcache', methods=['POST', 'GET'])
def generate_queriesvalue_memcahe():
    if request.method == 'POST':
        number = int(request.form["no"])
        value = int(request.form["value"])
        start = datetime.now()
        try:
            equake=mc.get('records1')
            print(equake)
        except (mc.MemcachedKeyTypeError, mc.MemcachedKeyNoneError,
                TypeError, mc.MemcachedKeyCharacterError,
                mc.MemcachedKeyError, mc.MemcachedKeyLengthError,
                mc.MemcachedStringEncodingError):
            print('error')
        if not equake:
            x='DB'
            while (number > 0):
                cur.execute("SELECT * FROM earthquake where mag >? ORDER BY RANDOM()", ('{}'.format(value),))
                rows=cur.fetchall()
                print(rows)
                mc.set('records1',rows,time=900)
                print(mc.get('records1'))
                print(number)
                number = number - 1
            time_taken = datetime.now() - start
            print(time_taken)
        else:
            time_taken = datetime.now() - start
            x = 'MemCache'
    return render_template("result.html",
                           msg="Time to generate random queries is {0} from {1}".format(time_taken,x))
if __name__ == '__main__':
    app.debug = True
    app.run()
