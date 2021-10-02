from flask import Flask
from flask import Flask, request, jsonify
import os

import lib.instrument as istr
import lib.interface as itf
import lib.lib as l

app = Flask(__name__)

# Get temperature
@app.route('/temperature', methods=['GET'])
def temp():
	instrument = istr.create_instrument(os.environ.get('PORT'))
	try:
		temp = itf.read_temperature(instrument)

		return '{"results": {"temperature": ' + str(temp) + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Read charging speed
@app.route('/charging-speed/read', methods=['GET'])
def charging_speed_read():
	instrument = istr.create_instrument(os.environ.get('PORT'))
	try:
		amps = itf.read_charging_amps(instrument)
		kw = l.convert_amps_to_kw(amps)

		return '{"results": {"charging_speed_kw": ' + str(kw) + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Set charging speed
@app.route('/charging-speed/set', methods=['POST'])
def charging_speed_set():
	instrument = istr.create_instrument(os.environ.get('PORT'))
	try:
		content = request.json
		kw = content["value"]

		amps = l.convert_kw_to_amps(kw)
		itf.write_charging_amps(instrument, amps)

		read_amps = itf.read_charging_amps(instrument)
		read_kw = l.convert_amps_to_kw(amps)

		if amps == read_amps:
			return '{"results": {"success": "Successfully changed charging speed to ' + str(read_kw) + ' kW."}}'
		else:
			return '{"error": {"message": "Charging speed not changed to expected value"}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Set charging allowed
@app.route('/charging-allowed/set', methods=['POST'])
def charging_allowed_set():
	instrument = istr.create_instrument(os.environ.get('PORT'))
	try:
		content = request.json
		allowed = content["value"]

		itf.write_charging_allowed(instrument, allowed)
		read_allowed = itf.read_charging_allowed(instrument)

		if allowed == read_allowed:
			return '{"results": {"success": "Successfully changed charging permission to ' + str(read_kw) + '."}}'
		else:
			return '{"error": {"message": "Charging permission not changed to expected value."}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Read charging allowed
@app.route('/charging-allowed/read', methods=['GET'])
def charging_allowed_read():
	instrument = istr.create_instrument(os.environ.get('PORT'))
	try:
		allowed = itf.read_charging_allowed(instrument)

		return '{"results": {"charging_permission": ' + str(allowed) + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

if __name__ == '__main__':
	app.run()
