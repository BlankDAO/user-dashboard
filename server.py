#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session, Response, redirect
from web3 import Web3, HTTPProvider
from datetime import timedelta
from io import BytesIO as IO
import nacl.encoding
import nacl.signing
import requests
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
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    g.db = client['blankdao']
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
    res = g.db.member.find_one({'account': account})
    if not res:
        return json.dumps({
            'status': True,
            'data': {
                'brightid_confirm': False
            }
        })
    del res['_id']
    return json.dumps({'status': True, 'data': res, 'brightid_confirm': True})


@app.route('/submit-member', methods=['POST'])
def submit_member():
    data = json.loads(request.data)
    if not verify_message(data['publicKey'], data['timestamp'],
                          data['signedMessage']):
        return json.dumps({'status': False, 'message': 'Invalid data'})
    data['points'] = 0
    data['credit'] = 0
    data['earned'] = 0
    data['brightid_score'] = brightid_score()
    data['account'] = check_eth_addr(data['account'])
    if not g.db.member.find_one(data['account']):
        return json.dumps({'status': False, 'message': 'Already exists'})
    g.db.member.insert_one(data)
    return json.dumps({
        'status': True,
    })


@app.route('/check-account', methods=['POST'])
def check_account():
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    res = g.db.referrers.find_one({'account': account})
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
    res = g.db.referrers.find_one({'account': account})
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
            'referrer': referrer,
            'account': account,
            'hash': data['hash'],
            'registered': False
        })
    return json.dumps({
        'msg': 'Your Address Submied Successfully',
        'status': True
    })


@app.route('/get-referrer', methods=['POST'])
def get_referrer():
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    doc = g.db.referrers.find({'account': account})
    if doc:
        if doc['registered']:
            return json.dumps({'referrer': doc['referrer'], 'status': True})
    return json.dumps({'msg': 'No referrer', 'status': False})


@app.route('/get-referred-investors', methods=['POST'])
def get_referred_investors():
    referred_investors = []
    data = json.loads(request.data)
    account = check_eth_addr(data['account'])
    docs = g.db.referrers.find({'referrer': account})
    for doc in docs:
        if doc['registered']:
            referred_investors.append(doc['account'])
    return json.dumps({
        'referred-investors': referred_investors,
        'status': True
    })


@app.route('/instagram-login')
def instagram_login():
    uri = config.INSTAGRAM_CLIENT[
        'auth_uri'] + '?client_id={0}&redirect_uri={1}&response_type=code'.format(
            config.INSTAGRAM_CLIENT['client_id'],
            config.INSTAGRAM_CLIENT['redirect_uri'])
    return redirect(uri)


@app.route('/instagram-auth')
def auth():
    config.INSTAGRAM_CLIENT.update({'code': request.args.get('code')})
    return Response(
        requests.post(
            config.INSTAGRAM_CLIENT['token_uri'],
            data=config.INSTAGRAM_CLIENT).text,
        status=200,
        mimetype='application/json')
    # resualt is:
    # {'access_token': '6253355905.0cfde61.4099f3d082a74dabac30271d5e66c840', 'user': {'id': '6253355905', 'username': 'hamidreza.zarepour', 'profile_picture': 'https://scontent.cdninstagram.com/vp/d5e9b26ffb35bca808a045fab87b55d3/5D24FE78/t51.2885-19/s150x150/45880528_202374717369019_3973935739212660736_n.jpg?_nc_ht=scontent.cdninstagram.com', 'full_name': 'Hamid reza zare pour', 'bio': 'Computer programmer.music lover', 'website': 'http://hrzp.lsbits.com/', 'is_business': false}}


def brightid_score():
    # TODO get scro from BrightID API
    return 0


def verify_message(public_key, message, sig):
    try:
        verify_key = nacl.signing.VerifyKey(
            public_key, encoder=nacl.encoding.URLSafeBase64Encoder)
        encoder = nacl.encoding.URLSafeBase64Encoder
        verify_key.verify(message, encoder.decode(sig))
        return True
    except:
        return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008, threaded=True)
