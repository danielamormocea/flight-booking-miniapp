from flask import Flask
from flask import request
import json
import random
import mysql.connector

app = Flask(__name__)



@app.route('/get_optimal_route', methods = ['GET', 'POST'])
def get_optimal_route():
    jsondata = request.get_json()
    data = json.loads(jsondata)

    source = data['source']
    destination = data['destination']
    maxFlights = data['maxFlights']
    departureDay = data['departureDay']
    
    cnx = mysql.connector.connect(user='user', password='password', host='db', port='3306', database='db')
    cursor = cnx.cursor()

    query = ("SELECT * FROM flights WHERE departureDay >= '%s'" % (departureDay))
    cursor.execute(query)
    records = cursor.fetchall()

    hashtable = {} #sursa : [dest1, dest2..]

    for row in records:
        if row[0] in hashtable:
            hashtable[row[0]].append(row)
        else:
            hashtable[row[0]] = [row]

    start = source
    end = destination
    minim = 99999
    first_flight = True
    queue = []
    route = []
    queue.append(([start], 0, []))
    
    while queue:
        path = queue.pop(0)
        node = path[0][-1]
        
        if node == end:
            if minim > path[1]:
                minim = path[1]
                route = path[2]

        if len(path[0]) >= int(maxFlights) + 1:
            continue

        for adj in hashtable.get(node, []):
            
            escala = 0
            if first_flight is True:
                if adj[2] != int(departureDay):
                    
                    continue
            else:
                prev_flight = path[2][-1]
                now = adj[2] * 24 + adj[3]
                prev = prev_flight[2] * 24 + prev_flight[3] + prev_flight[4]
                if prev > now:
                    continue
                else:
                    escala = now - prev

            new_path = list(path[0])
            new_path.append(adj[1])

            new_flight = list(path[2])
            new_flight.append(adj)
            queue.append((new_path, path[1] + escala + adj[4], new_flight))

        first_flight = False
    
    if len(route) == 0:
        return "Nu s-a gasit o ruta optima"
    else:
        return {"route":route}


@app.route('/book_ticket', methods = ['GET', 'POST'])
def book_ticket():
    jsondata = request.get_json()
    data = json.loads(jsondata)

    nr = data['nr']
    flight_ids = list(data['flight_ids'])

    cnx = mysql.connector.connect(user='user', password='password', host='db', port='3306', database='db')
    cursor = cnx.cursor()
    
    reservID = 0
    reservID += random.randint(100, 999)

    success = True

    for i in range(int(nr)):
        query = ("SELECT * FROM flights where flightID = '%s'" % (flight_ids[i]))
        cursor.execute(query)
        records = cursor.fetchall()
        #check seats
        if records[0][5] * 1.1 < records[0][7] + 1:
            print("Nu mai sunt locuri disponibile")
            success = False
            break
        else:
            
            update = ("UPDATE flights SET numberOfReservations = '%s' WHERE flightID = '%s'" % (records[0][7] + 1, flight_ids[i]))
            cursor.execute(update)

            add_reservation = ("INSERT INTO reservations"
                        "(reservID, flightID)"
                        "VALUES (%s, %s)")
            data_reserv = (reservID, flight_ids[i])
            cursor.execute(add_reservation, data_reserv)
                                    
    if success is False:
        cnx.rollback()
        return {"reservation ID" : None}
    else:
        cnx.commit()
        return {"reservation ID" : reservID }

@app.route('/buy_ticket', methods = ['GET', 'POST'])
def buy_ticket():

    try:
        jsondata = request.get_json()
        data = json.loads(jsondata)
        reservID = int(data['reservID'])

        cnx = mysql.connector.connect(user='user', password='password', host='db', port='3306', database='db')
        cursor = cnx.cursor()

        query = ("SELECT * FROM reservations WHERE reservID = '%s'" % (reservID))
        cursor.execute(query)
        records = cursor.fetchall()
        boarding_pass = []

        for record in records:
            flightID = record[1]
            query = ("SELECT * FROM flights WHERE flightID = '%s'" % (flightID))
            cursor.execute(query)
            res = cursor.fetchall()
            boarding_pass.append(res)


            update = ("UPDATE flights SET numberOfSeats = '%s' WHERE flightID = '%s'" % (res[0][5] - 1, flightID))
            cursor.execute(update)

        query = ("DELETE FROM reservations WHERE reservID = '%s'" % (reservID))
        cursor.execute(query)
        cnx.commit()
    except:
        return "Something went wrong. Maybe you used the reservation already"

    return {"ticket":boarding_pass}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
