import argparse
import json
from datetime import datetime

def log_ride(km: float, date=None):
    if not validate_date_time_format(date):
        print("Invalid date and time format. Please use 'DD-MM-YY, HH'.")
        return

    try:
        with open("rides/rides.json", "r") as file:
            rides = json.load(file)
    except FileNotFoundError:
        rides = []

    if date == None:
        date = datetime.now().strftime("%d-%m-%y, %H")
        rides.append({"date": date, "km": km})
    else:
        date = datetime.strptime(date, "%d-%m-%y, %H")
        date = datetime.strftime(date, "%d-%m-%y, %H")
        rides.append({"date": date, "km": km})

    with open("rides/rides.json", "w") as file:
        json.dump(rides, file, indent=4)
    print(f"On {date}:00, {km} km logged.")

def validate_date_time_format(date_time: str) -> bool:
    try:
        valid_date_time = datetime.strptime(date_time, "%d-%m-%y, %H")
        return True
    except ValueError:
        return False

def get_all_rides() -> list:
    all_rides = []
    try:
        with open("rides/rides.json", "r") as file:
            rides = json.load(file)
            rides.sort(key=lambda ride: datetime.strptime(ride["date"], "%d-%m-%y, %H"))
            for ride in rides:
                print(f"Date: {ride["date"]}:00 - {ride["km"]} km")
                all_rides.append(ride)

    except FileNotFoundError:
        print("No rides logged yet.")
    return all_rides

def get_total_km() -> float:
    total_km = 0.0
    try:
        with open("rides/rides.json", "r") as file:
            rides = json.load(file)
            for ride in rides:
                total_km += ride["km"]

    except FileNotFoundError:
        print("No rides logged yet.")

    print(f"Total kilometers: {total_km}")
    return total_km

def main():
    parser = argparse.ArgumentParser(description="Track bike ride data.")
    subparsers = parser.add_subparsers(dest="command", help="commands")

    log_parser = subparsers.add_parser("log", help="Log a new ride with (mandatory) km and (optional) date and time [DD-MM-YYYY, hh].")
    log_parser.add_argument("kilometers", type=float, help="Distance of ride in km in float value.")
    log_parser.add_argument("date_time", type=str, nargs="?", default=None, help="(Optional) Date and time of the ride [DD-MM-YYYY, hh] formated.")

    all_rides_parser = subparsers.add_parser("all", help="Display all logged rides.")

    total_parser = subparsers.add_parser("total", help="Display total kilometers of all rides.")

    args = parser.parse_args()

    match args.command:
        case "log":
            log_ride(args.kilometers, args.date_time)
        case "all":
            get_all_rides()
        case "total":
            get_total_km()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()