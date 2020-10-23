import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='user', password='password', host='db', port='3306', database='db')


cursor = cnx.cursor()

DB_NAME = 'db'
TABLES = {}
TABLES['flights'] = (
        "CREATE TABLE flights ("
        "source varchar(20) NOT NULL,"
        "destination varchar(20) NOT NULL,"
        "departureDay int(4) NOT NULL,"
        "departureHour int(5) NOT NULL,"
        "duration int(5) NOT NULL,"
        "numberOfSeats int(5) NOT NULL,"
        "flightID varchar(20) NOT NULL,"
        "numberOfReservations int(3) NOT NULL,"
        "PRIMARY KEY (`flightID`)"
        ") ENGINE=InnoDB")

TABLES['reservations'] = (
        "CREATE TABLE reservations ("
        "reservID int(3) NOT NULL,"
        "flightID varchar(20) NOT NULL"
        ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}:".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists")
        else:
            print(err.msg)
    else:
        print("OK")

while 1:
    action = input("TYPE A: Add flight \nTYPE B: Remove flights \nTYPE C: Show all \n")
    if "A" in action:
        source = input("Where from? ")
        destination = input("Where to? ")
        departureDay = input("When(day)? ")
        departureHour = input("When(hour)? ")
        duration = input("How long? ")
        numberOfSeats = input("Max capacity: ")
        flightID = input("Flight ID: ")
        
        try:
            add_flight = ("INSERT INTO flights"
                    "( source, destination, departureDay, departureHour, duration, numberOfSeats, flightID, numberOfReservations)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            data_flight = (source, destination, departureDay, departureHour, duration, numberOfSeats, flightID, 0)
            print(data_flight)
            cursor.execute(add_flight, data_flight)
            cnx.commit()
        except:
            print("Something went wrong. Retry")
            continue
    
    if "B" in action:
        rmv_flightID = input("ID flight to delete: ")
        remove_flight = ("DELETE FROM flights where flightID = '%s'" % (rmv_flightID))
        cursor.execute(remove_flight)
        
        cnx.commit()

    if "C" in action:
        query = ("SELECT * FROM flights")
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)



