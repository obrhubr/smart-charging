import requests

def getDate(dt):
    return dt.strftime("%Y-%m-%d") + "%20" + dt.strftime("%H:%M:%S")

def get_current_power(siteID, apiKey):
    timestart = getDate(datetime.now())
    timeend = getDate(datetime.now()+ datetime.timedelta(minutes = 10))

    url = "https://monitoringapi.solaredge.com/site/" + siteID + "/powerDetails?meters=PRODUCTION,CONSUMPTION&startTime=" + timestart + "&endTime=" + timeend + "&api_key=" + apiKey

    r = requests.get(url)
    jsonres = r.json()

    power_details = {}

    production_array = jsonres["powerDetails"]["meters"]
    for array in production_array:
        if array["type"] == "Production":
            power_details["production"] = array["values"][0]["value"]

        if array["type"] == "Consumption":
            power_details["consumption"] = array["values"][0]["value"]

    return power_details