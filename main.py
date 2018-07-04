import asyncio
from flask import Flask, request
import getopt
import logging
import os
import sys

from alert import PrometheusAlert
import xmpp

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd", ["debug"])
except getopt.GetoptError:
    print('main.py -d')
    sys.exit(2)

log.info("Starting Alertmanager Xmpp Notification")

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def prometheus_alert():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    msg = PrometheusAlert(request.data.decode()).plain()
    html = PrometheusAlert(request.data.decode()).html()
    xmpp.Send(msg)
    return '', 204

log.info("Start server")

app.run(host='0.0.0.0', debug=False)

log.info("Exit...")
