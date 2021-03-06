from flask import Flask, request, jsonify, Response
import os

import lib.instrument as istr
import lib.interface as itf
import lib.lib as l

app = Flask(__name__)

def log(string):
	print(str(string), flush=True)

# Get temperature
@app.route('/temperature', methods=['GET'])
def temp():
	try:
		instrument = istr.create_instrument()
	except:
		return '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'

	try:
		temp = itf.read_temperature(instrument)

		ret = '{"results": {"temperature": ' + str(temp) + '}}'
		log(ret)

		return ret
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'

# Read charging speed
@app.route('/charging-speed/read', methods=['GET'])
def charging_speed_read():
	try:
		instrument = istr.create_instrument()
	except:
		return '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'

	try:
		amps = itf.read_charging_amps(instrument)
		kw = l.convert_amps_to_kw(amps)

		ret = '{"results": {"charging_speed_kw": ' + str(kw) + ', "charging_speed_amps": ' + str(amps) + '}}'
		log(ret)

		return ret
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'

# Set charging speed
@app.route('/charging-speed/set', methods=['POST'])
def charging_speed_set():
	try:
		instrument = istr.create_instrument()
	except:
		return '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'

	try:
		content = request.json
		kw = content["value"]

		amps = round(l.convert_kw_to_amps(kw))
		itf.write_charging_amps(instrument, amps)

		read_amps = itf.read_charging_amps(instrument)
		read_kw = l.convert_amps_to_kw(amps)

		ret = '{"results": {"charging_speed_read_kw": ' + str(read_kw) + ', "charging_speed_read_amps": ' + str(read_amps) + ', "charging_speed_write_amps": ' + str(amps) + '}}'
		log(ret)

		return ret
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'

# Set charging allowed
@app.route('/charging-allowed/set', methods=['POST'])
def charging_allowed_set():
	try:
		instrument = istr.create_instrument()
	except:
		return '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'

	try:
		content = request.json
		allowed = content["value"]

		itf.write_charging_allowed(instrument, allowed)
		read_allowed = itf.read_charging_allowed(instrument)

		if allowed == read_allowed:
			ret = '{"results": {"success": "Successfully changed charging permission to ' + str(read_allowed) + '."}}'
			log(ret)
			return ret
		else:
			ret = '{"error": {"message": "Charging permission not changed to expected value."}}'
			log(ret)
			return ret
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'

# Read charging allowed
@app.route('/charging-allowed/read', methods=['GET'])
def charging_allowed_read():
	try:
		instrument = istr.create_instrument()
	except:
		ret = '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'
		log(ret)
		return ret
		
	try:
		allowed = itf.read_charging_allowed(instrument)

		ret = '{"results": {"charging_permission": ' + str(allowed) + '}}'
		log(ret)
		return ret
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'
		log(ret)
		return ret

# Read charging allowed
@app.route('/prometheus', methods=['GET'])
def prometheus():
	"""
	# TYPE health_check gauge
	sm_health_check 1
	
	# TYPE device_temperature gauge
	sm_device_temperature 29

	# TYPE current_charging_speed gauge
	sm_current_charging_speed 6

	# TYPE charging_allowed gauge
	sm_charging_allowed 1
	"""
	try:
		instrument = istr.create_instrument()
	except:
		ret = '{"error": {"message": ' + '"Could not connect via modbus."' + '}}'
		log(ret)
		return ret

	try:
		temperature = itf.read_temperature(instrument)
		amps = itf.read_charging_amps(instrument)
		speed = l.convert_amps_to_kw(amps)
		allowed = itf.read_charging_allowed(instrument)

		ret = '# TYPE sm_health_check gauge\nsm_health_check 1 \n# TYPE sm_device_temperature gauge\nsm_device_temperature ' + str(temperature) + ' \n# TYPE sm_current_charging_speed gauge\nsm_current_charging_speed ' + str(speed) + ' \n# TYPE sm_charging_allowed gauge\nsm_charging_allowed ' + str(allowed) + ''
		log(ret)
		return Response(ret, mimetype='text/plain')
	except IOError as e:
		return '{"error": {"message": "' + str(e) + '"}}'
		log(ret)
		return ret


if __name__ == '__main__':
	app.run()
