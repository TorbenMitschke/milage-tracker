import argparse
import json
from datetime import datetime

def log_ride(km: float, date: str = datetime.now().strftime("%d-%m-%y, %H")):
    try:
        with open("rides/rides.json", "r") as file:
            rides = json.load(file)
    except FileNotFoundError:
        rides = []

    rides.append({"date": date, "km": km})

    with open("rides/rides.json", "w") as file:
        json.dump(rides, file, indent=4)
    print(f"On {date}, {km} km logged.")

def get_total_km() -> float:
    total_km = 0
    try:
        with open("rides/ride.json", "r") as file:
            rides = json.load(file)
            for ride in rides:
                total_km += ride["km"]

    except FileNotFoundError:
        print("No rides logged yet.")

    print(f"Total kilometers: {total_km}")
    return total_km
