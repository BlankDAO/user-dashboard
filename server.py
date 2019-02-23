#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session
from web3 import Web3, HTTPProvider
from io import BytesIO as IO
from datetime import timedelta
import pymongo
import config
import gzip
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class ErrorToClient(Exception):
    pass


def gzip_content(response):
    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' not in accept_encoding.lower():
        return response
    response.direct_passthrough = False
    if (response.status_code < 200 or response.status_code >= 300
            or 'Content-Encoding' in response.headers):
        return response
    gzip_buffer = IO()
    gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)
    return response


@app.errorhandler(ErrorToClient)
def error_to_client(error):
    return json.dumps({
        'msg': error.args[0],
        'args': error.args[1:],
        'status': False
    })


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    g.db = client["blankdao"]
    g.w3 = Web3(HTTPProvider(config.INFURA_URL))


@app.after_request
def after_request(response):
    return gzip_content(response)


@app.teardown_request
def teardown_request(exception):
    pass


def check_eth_addr(address):
    try:
        return g.w3.toChecksumAddress(address)
    except Exception:
        raise ErrorToClient('Invalid Address')


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.route('/check-account', methods=['POST'])
def check_account():
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    res = g.db.referrers.find_one({"account": account})

    if res:
        if res['registered']:
            raise ErrorToClient('Your account has already been registered',
                                {'referrer': res['referrer']})
    return json.dumps({'status': True, 'msg': 'Allow'})


@app.route('/add-referrer', methods=['POST'])
def add_referrer():
    data = json.loads(request.data)

    referrer = check_eth_addr(data['referrer'])
    account = check_eth_addr(data['account'])
    res = g.db.referrers.find_one({"account": account})
    if res:
        if res['registered']:
            raise ErrorToClient('Your account has already been registered')
        else:
            g.db.referrers.update_one({
                '_id': res['_id']
            }, {'$set': {
                'referrer': referrer
            }},
                                      upsert=False)
    else:
        g.db.referrers.insert_one({
            "referrer": referrer,
            "account": account,
            "registered": False
        })
    return json.dumps({
        'msg': 'Your Address Submied Successfully',
        'status': True
    })


@app.route('/get-referrer', methods=['POST'])
def get_referrer():
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    mydoc = g.db.referrers.find({"account": account})
    if mydoc:
        if mydoc['registered']:
            return json.dumps({'referrer': mydoc['referrer'], 'status': True})
    return json.dumps({'msg': 'No referrer', 'status': False})


if __name__ == '__main__':
    app.run(debug=True, port=5008, threaded=True)
