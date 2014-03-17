import urllib2
import logging

import gevent
import gevent.pywsgi
from flask import Flask, request, abort


app = Flask("es_mon")
log = logging.getLogger("")
# app.debug = True


allowed_paths = set(["_cluster/state",
                     "panda/_mapping",
                     "panda/_status",
])


@app.route("/<path:path>")
def proxy(path):
    print path
    if path not in allowed_paths:
        abort(401)
    path = "http://localhost:9200/" + path
    return urllib2.urlopen(path).read()


@app.route("/")
def index():
    return proxy("_cluster/state")


def http_server():
    http_server = gevent.pywsgi.WSGIServer(
        ('', 8002), app)
    http_server.start()
    print "started http_server"

if __name__ == "__main__":
    http_server()
    while 1:
        gevent.sleep(5)
