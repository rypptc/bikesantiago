import requests
import json
from django.utils import timezone
from bikes_info.models import Station
import datetime


def printdata(request=None):
    response = requests.get('http://api.citybik.es/v2/networks/bikesantiago')
    data = json.loads(response.content.decode('utf-8'))
    with open('bikes_data.txt', 'w') as f:
        f.write(json.dumps(data, indent=4))

def get_payment_choices():
    response = requests.get('http://api.citybik.es/v2/networks/bikesantiago')
    json_data = response.json()
    payments = set()

    for station in json_data['network']['stations']:
        payment = station.get('extra', {}).get('payment')
        if payment:
            payments.add(tuple(payment))

    print(payments)


def populate_stations():
    response = requests.get('http://api.citybik.es/v2/networks/bikesantiago')
    json_data = response.json()

    for station_data in json_data['network']['stations']:
        station = Station()
        station.station_id = station_data['id']
        station.name = station_data['name']
        station.address = station_data['extra']['address']
        station.post_code = station_data['extra'].get('post_code', '')
        station.latitude = station_data['latitude']
        station.longitude = station_data['longitude']
        station.free_bikes = station_data['free_bikes']
        station.has_ebikes = station_data['extra']['ebikes']
        station.normal_bikes = station_data['extra']['normal_bikes']
        station.slots = station_data['extra']['slots']
        station.empty_slots = station_data['empty_slots']
        station.payment = station_data['extra']['payment']
        station.payment_terminal = station_data['extra']['payment-terminal']
        station.renting = station_data['extra']['renting']
        station.returning = station_data['extra']['returning']
        station.last_updated = timezone.make_aware(datetime.datetime.fromtimestamp(int(station_data['extra']['last_updated'])))
        station.uid = station_data['extra']['uid']
        station.timestamp = timezone.now()
        station.save()