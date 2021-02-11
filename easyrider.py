# Write your awesome code here
import json
import re


types_dict = {"bus_id": [0, int],
              "stop_id": [0, int],
              "stop_name": [0, str],
              "next_stop": [0, int],
              "stop_type": [0, str],
              "a_time": [0, str]}


def type_validation(inp):
    for data in inp:
        for i in types_dict:
            if type(data[i]) != types_dict[i][1]:
                types_dict[i][0] += 1
            elif i == "stop_type" and len(data[i]) > 1:
                types_dict[i][0] += 1
            elif i != "stop_type" and data[i] == "":
                types_dict[i][0] += 1
    print(f'Type and required field validation: {sum(value[0] for value in types_dict.values())} errors')
    for i in types_dict:
        print(f'{i}: {types_dict[i][0]}')


def format_validation(inp):
    for data in inp:
        if not re.match(r"[A-Z].+ (Road|Avenue|Boulevard|Street)$", data["stop_name"]):
            types_dict["stop_name"][0] += 1
        if not re.match(r"[SOF]?$", data["stop_type"]):
            types_dict["stop_type"][0] += 1
        if not re.match("[0-2][0-9]:[0-6][0-9]$", data["a_time"]):
            types_dict["a_time"][0] += 1
    print(f'Format validation: {sum(value[0] for value in types_dict.values())} errors')
    print(f'stop_name: {types_dict["stop_name"][0]}')
    print(f'stop_type: {types_dict["stop_type"][0]}')
    print(f'a_time: {types_dict["a_time"][0]}')


def number_of_stops(inp):
    lines = {}
    for data in inp:
        if data["bus_id"] not in lines:
            lines[data["bus_id"]] = 1
        else:
            lines[data["bus_id"]] += 1
    print('Line names and number of stops:')
    for line, stops in lines.items():
        print(f'bus_id: {line}, stops: {stops}')


def start_end_validation(inp):
    bus_lines = set()
    for data in inp:
        bus_lines.add(data["bus_id"])
    for line in bus_lines:
        start_counter = 0
        finish_counter = 0
        for data in inp:
            if data["bus_id"] == line and data["stop_type"] == "S":
                start_counter += 1
            if data["bus_id"] == line and data["stop_type"] == "F":
                finish_counter += 1
        if start_counter != 1 or finish_counter != 1:
            print(f"There is no start or end stop for the line: {line}")
            exit()


def start_finish_count(inp):
    start_stops = set()
    finish_stops = set()
    bus_lines = set()
    transfer_stops = set()
    seen = set()
    for data in inp:
        bus_lines.add(data["bus_id"])
        if data["stop_type"] == "S":
            start_stops.add(data["stop_name"])
        elif data["stop_type"] == "F":
            finish_stops.add(data["stop_name"])
        if data["stop_name"] in seen:
            transfer_stops.add(data["stop_name"])
        else:
            seen.add(data["stop_name"])
    print(f"Start stops: {len(start_stops)} {list(sorted(start_stops))}")
    print(f"Transfer stops: {len(transfer_stops)} {list(sorted(transfer_stops))}")
    print(f"Finish stops: {len(finish_stops)} {list(sorted(finish_stops))}")


def arrival_time_test(inp):
    bus_lines = set()
    stops_dict = []
    failed = False
    print("Arrival time test:")
    for data in inp:
        bus_lines.add(data["bus_id"])
    for line in bus_lines:
        for data in inp:
            if data["bus_id"] == line:
                stops_dict.append([data["stop_id"], data["a_time"]])
        i = 0
        while i < (len(stops_dict) - 1):
            if stops_dict[i][1] > stops_dict[i+1][1]:
                for data in inp:
                    if data["bus_id"] == line and data["stop_id"] == stops_dict[i+1][0]:
                        print(f'bus_id line {line}: wrong time on station {data["stop_name"]}')
                        failed = True
                break
            else:
                i += 1
        stops_dict.clear()
    if not failed:
        print("OK")


def on_demand_stops_test(inp):
    transfer_stops = set()
    seen = set()
    wrong_stops = set()
    for data in inp:
        if data["stop_name"] in seen:
            transfer_stops.add(data["stop_name"])
        else:
            seen.add(data["stop_name"])
    for data in inp:
        if data["stop_type"] == "O" and data["stop_name"] in transfer_stops:
            wrong_stops.add(data["stop_name"])
    print("On demand stops test:")
    print(f"Wrong stop type: {list(sorted(wrong_stops))}" if len(wrong_stops) > 0 else "OK")


input_data = json.loads(input())
# type_validation(input_data)
# format_validation(input_data)
# number_of_stops(input_data)
# start_end_validation(input_data)
# start_finish_count(input_data)
# arrival_time_test(input_data)
on_demand_stops_test(input_data)
