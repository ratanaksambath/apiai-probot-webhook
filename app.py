#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Change locally")
    print("Request:")
    print(json.dumps(req, indent=4))

    res = postSheetsu(req)
    print(res)
    # res = json.dumps(res, indent=4)
    # print(res)
    # r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    # return r
def postSheetsu(req):
    if req.get("result").get("action") != "probotSheets":
        return{}
    url = "https://sheetsu.com/apis/v1.0/4bec9339fcd9"
    created_at = req.get("result").get("timestamp")
    project_title = req.get("result").get("result").get("parameters").get("project_title")
    project_manager_name = req.get("result").get("result").get("parameters").get("project_manager_name")
    values = {'created_at': created_at, 'project_title': project_title,'project_manager_name':project_manager_name}
    print(values)
    data = urllib.urlencode(values)
    res = urllib.urlopen(url,data)
    print res.read()
    return res

def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    result = urllib.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
