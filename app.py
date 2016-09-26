#!/usr/bin/env python

import urllib
import urllib2
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
    print("Request:")
    print(json.dumps(req, indent=4))
    res = postSheetsu(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def postSheetsu(req):
    if req.get("result").get("action") != "probotSheets":
        return{}
    url = "https://sheetsu.com/apis/v1.0/4bec9339fcd9"
    # created_at = req.get("result").get("timestamp")
    # project_title = req.get("result").get("parameters").get("project_title")
    # project_manager_name = req.get("result").get("parameters").get("project_manager_name")
    values = {'created_at': 'December 13, 2016', 'project_title': 'How do you turn this on','project_manager_name': 'NEMO'}
    data = urllib.urlencode(values)
    sheet_request = urllib2.Request(url,data)
    sheet_response = urllib2.urlopen(sheet_request)
    status_code = sheet_response.getcode()
    if status_code != 201:
        return {
                "speech": "Can't seem to create a new project to your google sheet",
                "displayText": "Can't seem to create a new project to your google sheet",
                # "data": data,
                # "contextOut": [],
                "source": "probotSheets-webhook-sample"
        }
    else:
        return {
                "speech": "Your project has been added to your excel sheet in google drive",
                "displayText": "Your project has been added to your excel sheet in google drive",
                # "data": data,
                # "contextOut": [],
                "source": "probotSheets-webhook-sample"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
