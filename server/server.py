#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session, send_from_directory
from insta_pic_genrator import InstagramQrCode
from web3 import Web3, HTTPProvider
from datetime import timedelta
from io import BytesIO as IO
import nacl.encoding
import nacl.signing
import twitter
import pymongo
import config
import gzip
import json
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='../ui')
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
    g.blank_token_contract = g.w3.eth.contract(
        address=config.BLANK_TOKEN_ADDR, abi=config.BLANK_TOKEN_ABI)


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
    return redirect('/index.html')


@app.route('/get-info', methods=['POST'])
def get_info():
    data = json.loads(request.data)
    if 'account' not in data:
        raise ErrorToClient('Error in connection')
    account = check_eth_addr(data['account'])
    res = g.db.members.find_one({'account': account})
    if not res:
        return json.dumps({
            'status': True,
            'data': {
                'brightid_confirm': False
            }
        })
    for key in ['_id', 'signedMessage', 'timestamp', 'instagram', 'twitter']:
        del res[key]
    res['BDT_balance'] = blank_token_balance(check_eth_addr(data['account']))
    return json.dumps({'status': True, 'data': res, 'brightid_confirm': True})


@app.route('/submit-member', methods=['POST'])
def submit_member():
    data = json.loads(request.data)
    if g.db.members.find_one(data['publicKey']):
        return json.dumps({'status': False, 'msg': 'Already exists'})
    if not verify_message(data['publicKey'], data['timestamp'],
                          data['signedMessage']):
        return json.dumps({'status': False, 'msg': 'Invalid data'})
    data['points'] = 0
    data['credit'] = 0
    data['earned'] = 0
    data['instagram'] = None
    data['instagram_confirmation'] = False
    data['twitter'] = None
    data['twitter_confirmation'] = False
    data['brightid_level_reached'] = True if data['score'] >= 90 else False
    data['account'] = check_eth_addr(data['account'])
    g.db.members.insert_one(data)
    return json.dumps({'status': True})


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
        'msg': 'Your Address Submited Successfully',
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


@app.route('/submit-instagram', methods=['POST'])
def submit_instagram():
    data = json.loads(request.data)
    public_key = data['publicKey']
    res = g.db.members.find_one({'publicKey': public_key})
    if not res:
        return json.dumps({'msg': 'User Not Found', 'status': False})
    if res['instagram_confirmation']:
        return json.dumps({
            'msg': 'Instagram registered before',
            'status': False
        })
    g.db.members.update_one({
        'publicKey': public_key
    }, {'$set': {
        'instagram': data['instagram_username']
    }},
    upsert=False)
    return json.dumps({
        'msg':
        'Your Instagram Username Submited Successfully. It will be confirmed in next 24 hours',
        'status':
        True
    })


@app.route('/twitter-login', methods = ['POST'])
def twitter_login():
    data = json.loads(request.data)
    pk = data['publicKey']
    res = g.db.members.find_one({'publicKey': pk})
    if not res:
        raise ErrorToClient('Cant find your publicKey')

    if res['twitter_confirmation'] == True:
        raise ErrorToClient('Your twitter account submited')

    url = twitter.twitter_get_oauth_request_token(pk)
    return json.dumps({
        'url': url,
        'msg': 'Done Successfully',
        'status': True
    })


@app.route('/twitter-authorized')
def twitter_authorized():
    res = g.db.twitter_temp.find_one({'resource_owner_key': request.args.get('oauth_token')})
    if not res:
        raise ErrorToClient('Wrong oauth_token')

    key = res['resource_owner_key']
    secret = res['resource_owner_secret']
    access_token_list = twitter.twitter_get_oauth_token(request.args.get('oauth_verifier'), key, secret)
    user_data = twitter.twitter_get_access_token(access_token_list)
    user_data['publicKey'] = res['publicKey']
    g.db.twitter.insert_one(user_data)
    update_member_twitters_state(res['publicKey'])
    g.db.twitter_temp.delete_one({'_id': res['_id']})
    return redirect('/index.html')



@app.route('/instagram-image', methods = ['POST'])
def instagram_image():
    print('dfsdfsdfsd***********************')
    data = json.loads(request.data)
    pk = data['publicKey']
    res = g.db.members.find_one({'publicKey': pk})
    if not res:
        raise ErrorToClient('Cant find your publicKey')

    image = InstagramQrCode()
    file_name = image.get_file(pk)
    return json.dumps({
        'file_name': file_name,
        'status': True
    })
    # return send_file('../insta-images/' + file_name + '.png', attachment_filename="img.png")


@app.route('/instagram-image/<file>')
def get_instagram_image(file):
    return send_from_directory('../insta-images', file + '.png')


def update_member_twitters_state(publicKey):
    res = g.db.members.find_one({'publicKey': publicKey})
    if not res:
        raise ErrorToClient('something wrong, your public key is not defined')

    g.db.members.update_one({
        '_id': res['_id']
    }, {'$set': {
        'twitter_confirmation': True
    }},
    upsert=False)


def brightid_score():
    # TODO get scro from BrightID API ASAP
    pass


def verify_message(public_key, timestamp, sig):
    message = bytearray(
        public_key + config.BLANKDAO_PUBLIC_KEY + str(timestamp), 'utf8')

    try:
        verify_key = nacl.signing.VerifyKey(
            public_key, encoder=nacl.encoding.URLSafeBase64Encoder)
        encoder = nacl.encoding.URLSafeBase64Encoder
        verify_key.verify(message, encoder.decode(sig))
        return True
    except Exception:
        return False


def blank_token_balance(account):
    account = check_eth_addr(account)
    func = g.blank_token_contract.functions.balanceOf(account)
    result = func.call({'from': account})
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008, threaded=True)
