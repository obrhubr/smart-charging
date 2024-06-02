import lib.instrument as istr
import lib.interface as itf
import lib.lib as l

import json
from datetime import datetime
import requests

import os

def charging_speed_read():
	try:
		instrument = istr.create_instrument()
	except:
		return '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'

	try:
		amps = itf.read_charging_amps(instrument)
		kw = l.convert_amps_to_kw(amps)

		return kw
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'
	
def get_time():
	try:
		instrument = istr.create_instrument()
	except:
		print('{"error": {"message": ' + '"Could not connect via modbus."' + '}}')

	try:
		time = itf.read_charging_time(instrument)
		
		return time
	except IOError as e:
		print('{"error": {"message": "' + str(e) + '"}}')

def read_json_from_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
def write_json_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def ms_to_hms(milliseconds):
    # Convert milliseconds to seconds
    seconds = milliseconds / 1000

    # Calculate hours, minutes, and seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return hours, minutes, seconds

def send_log(plugged_in, current, charging_time):
	url = 'https://api.logsnag.com/v1/log'

	# JSON data to be sent in the POST request
	hours, minutes, seconds = ms_to_hms(charging_time)
	json_data = {
		'project': 'charging',
		'channel': 'status',
		'event': "plugged_in" if plugged_in else "plugged_out",
		'description': "The car was plugged into the charging station." if plugged_in else "The car was plugged out from the charging station.",
		'icon': '🔋' if plugged_in else '🚨',
		'notify': True,
		'tags': {
			'power': current,
			'charging_time': f"{hours} hours, {minutes} minutes, {seconds} seconds"
		}
	}

	# Bearer token for authentication
	bearer_token = ''

	# Headers containing the Bearer token
	headers = {
		'Authorization': f'Bearer {os.environ["LOGSNAG"]}',
		'Content-Type': 'application/json'
	}

	# Sending the POST request
	response = requests.post(url, json=json_data, headers=headers)

	return response

def main():
	old_data = read_json_from_file('charging.json')
	data = {
		"charging_time": get_time(),
		"timestamp": datetime.timestamp(datetime.now()) * 1000,
		"status": False
	}

	real_diff = abs(data["timestamp"] - old_data["timestamp"])
	charging_diff = abs(data["charging_time"] - old_data["charging_time"])

	# if difference between real time elapsed and charging time
	# is smaller than 10s write new json to file
	# assumes that this gets called less frequently than once a minute
	if abs(real_diff - charging_diff) < 60 * 1000:
		data["status"] = True
		pass

	# if car has only been plugged in for 10 minutes
	# and different status than before
	if data["charging_time"] < 10 * 60 * 1000 and data["status"] != old_data["status"]:
		# send log that car has been plugged in
		send_log(True, charging_speed_read(), data["charging_time"])

	# if the charging diff = 0 -> plugged out
	# and different status than before
	elif charging_diff < 1000 and data["status"] != old_data["status"]:
		# send log that car has been plugged out
		send_log(False, charging_speed_read(), data["charging_time"])

	# write new data to file
	write_json_to_file(data, "charging.json")

main()