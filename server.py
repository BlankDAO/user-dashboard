#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session
from web3 import Web3, HTTPProvider
from datetime import timedelta
from io import BytesIO as IO
from time import time as now
from config import api_key
from hashlib import sha256
import pymongo
import config
import uuid
import gzip
from pprint import pprint as pp
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def check_api_key(_api_key, timestamp):
    key = str(timestamp) +  ' - ' + api_key
    print(sha256(key.encode('utf-8')).hexdigest())
    if sha256(key.encode('utf-8')).hexdigest() == _api_key:
        return True
    return False


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


@app.route('/get-info', methods=['POST'])
def get_info():
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    res = g.db.member.find_one({"account": account})
    print(type(res))
    if res:
        del res['_id']
        pp(res)
        return json.dumps({'status': True, "data": res, "brightid_confirm": True})

    return json.dumps({
        'status': True,
        "data": {
            "brightid_confirm": False
        }
    })


@app.route('/submit-member', methods=['POST'])
def submit_member():
    data = json.loads(request.data)

    data['points'] = 33
    data['credit'] = 44
    data['earned'] = 10
    data['brightid_score'] = 80
    data['account'] = check_eth_addr(data['account'])
    g.db.member.insert_one(data)

    return json.dumps({
        'status': True,
    })


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
                'referrer': referrer,
                'hash': data['hash'],
            }},
                                      upsert=False)
    else:
        g.db.referrers.insert_one({
            "referrer": referrer,
            "account": account,
            "hash": data["hash"],
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
    doc = g.db.referrers.find({"account": account})
    if doc:
        if doc['registered']:
            return json.dumps({'referrer': doc['referrer'], 'status': True})
    return json.dumps({'msg': 'No referrer', 'status': False})


@app.route('/get-referred-investors', methods=['POST'])
def get_referred_investors():
    referred_investors = []
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    docs = g.db.referrers.find({"referrer": account})
    for doc in docs:
        if doc['registered']:
            referred_investors.append(doc['account'])
    return json.dumps({
        'referred-investors': referred_investors,
        'status': True
    })


client = {
    'client_id'      : '',
    'client_secret'  : '',
    'grant_type'     : 'authorization_code',
    'redirect_uri'   : 'http://104.207.144.107:8000/instagram-auth',
    'auth_uri'       : 'https://api.instagram.com/oauth/authorize/',
    'token_uri'      : 'https://api.instagram.com/oauth/access_token/'
}

@app.route('/instagram-login')
def instagram_login():
    uri = client['auth_uri'] + '?client_id={0}&redirect_uri={1}&response_type=code'.format(client['client_id'], client['redirect_uri'])
    return flask.redirect(uri)

@app.route('/instagram-auth')
def auth():
    client.update({'code': flask.request.args.get('code')})
    return flask.Response(requests.post(client['token_uri'], data=client).text, status=200, mimetype='application/json')
    # resualt is:
        # {"access_token": "6253355905.0cfde61.4099f3d082a74dabac30271d5e66c840", "user": {"id": "6253355905", "username": "hamidreza.zarepour", "profile_picture": "https://scontent.cdninstagram.com/vp/d5e9b26ffb35bca808a045fab87b55d3/5D24FE78/t51.2885-19/s150x150/45880528_202374717369019_3973935739212660736_n.jpg?_nc_ht=scontent.cdninstagram.com", "full_name": "Hamid reza zare pour", "bio": "Computer programmer.music lover", "website": "http://hrzp.lsbits.com/", "is_business": false}}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0' , port=5008, threaded=True)
