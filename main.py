from flask import Flask
from flask import Flask, request, jsonify

import lib.instrument as istr
import lib.interface as itf
import lib.lib as l

app = Flask(__name__)

# Get temperature
@app.route('/temperature', methods=['GET'])
def temp():
	global instrument
	try:
		temp = itf.read_temperature(instrument)

		return '{"results": {"temperature": ' + temp + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Read charging speed
@app.route('/charging-speed/read', methods=['GET'])
def charging_speed_read():
	global instrument
	try:
		amps = itf.read_charging_amps(instrument)
		kw = l.convert_amps_to_kw(amps)

		return '{"results": {"charging_speed_kw": ' + kw + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Set charging speed
@app.route('/charging-speed/set', methods=['GET', 'POST'])
def charging_speed_set():
	global instrument
	try:
		content = request.json
		kw = content["value"]

		amps = l.convert_kw_to_amps(kw)
		itf.write_charging_amps(instrument, amps)

		read_amps = itf.read_charging_amps(instrument)
		read_kw = l.convert_amps_to_kw(amps)

		if amps == read_amps:
			return '{"results": {"success": "Successfully changed charging speed to ' + read_kw + ' kW."}}'
		else:
			return '{"error": {"message": "Charging speed not changed to expected value"}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Set charging allowed
@app.route('/charging-allowed/set', methods=['GET', 'POST'])
def charging_allowed_set():
	global instrument
	try:
		content = request.json
		allowed = content["value"]

		itf.write_charging_allowed(instrument, allowed)
		read_allowed = itf.read_charging_allowed(instrument)

		if allowed == read_allowed:
			return '{"results": {"success": "Successfully changed charging permission to ' + read_kw + '."}}'
		else:
			return '{"error": {"message": "Charging permission not changed to expected value."}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

# Read charging allowed
@app.route('/charging-allowed/read', methods=['GET'])
def charging_allowed_read():
	global instrument
	try:
		allowed = itf.read_charging_allowed(instrument)

		return '{"results": {"charging_permission": ' + allowed + '}}'
	except IOError as e:
		return '{"error": {"message": ' + str(e) + '}}'

if __name__ == '__main__':
	instrument = istr.create_instrument()
    app.run()