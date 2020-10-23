import sys
import json
import requests


while 1:
    action = input("A - optimal route \nB - bookTicket \nC - buyTicket\n")
    if "A" in action:
        source = input("Source: ")
        destination = input("Destination: ")
        maxFlights = input("How many flights? ")
        departureDay = input("When? ")
        
        json1 = {'source': source, 'destination': destination, 'maxFlights': maxFlights, 'departureDay': departureDay}
        tosend = json.dumps(json1)
        res = requests.post("http://server:5000/get_optimal_route", json = tosend)
        print(res.text)

    if "B" in action:
        nr = input("How many flights?" )
        flight_ids = []
        for i in nr:
            ids = input("Give flight id: ")
            flight_ids.append(ids)

        json1 = {'nr': nr, 'flight_ids': flight_ids}
        tosend = json.dumps(json1)
        res = requests.post("http://server:5000/book_ticket", json = tosend)
        print(res.text)

    if "C" in action:
        reservID = input ("Give Reservation ID: ")
        creditCard = input("Credit card information: ")

        json1 = {'reservID': reservID, 'creditCard': creditCard}
        tosend = json.dumps(json1)
        res = requests.post("http://server:5000/buy_ticket", json = tosend)
        print(res.text)
