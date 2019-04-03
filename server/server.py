#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session, send_from_directory, jsonify
from insta_pic_genrator import InstagramQrCode
from web3 import Web3, HTTPProvider
from datetime import timedelta
from io import BytesIO as IO
import nacl.encoding
import requests
import nacl.signing
import twitter
import pymongo
import config
import redis
import gzip
import json
import os

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
)

app = Flask(__name__,
            static_url_path='',
            static_folder='../ui')
app.secret_key = os.urandom(24)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Setup the flask-jwt-extended extension.
ACCESS_EXPIRES = timedelta(minutes=10)
REFRESH_EXPIRES = timedelta(days=10)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

# Setup our redis connection for storing the blacklisted tokens
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'


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
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    g.db = client['blankdao']
    # g.w3 = Web3(HTTPProvider(config.INFURA_URL))
    # g.blank_token_contract = g.w3.eth.contract(
    #     address=config.BLANK_TOKEN_ADDR, abi=config.BLANK_TOKEN_ABI)


@app.after_request
def after_request(response):
    return gzip_content(response)


@app.teardown_request
def teardown_request(exception):
    pass


def check_eth_addr(address):
    try:
        g.w3 = Web3(HTTPProvider(config.INFURA_URL))
        return g.w3.toChecksumAddress(address)
    except Exception:
        raise ErrorToClient('Invalid Address')


@app.route('/')
def index():
    return redirect('/index.html')


@app.route('/get-info', methods=['POST'])
@jwt_required
def get_info():
    data = json.loads(request.data)
    if 'publicKey' not in data:
        raise ErrorToClient('Error in connection - No publicKey Founded')
    # TODO: check if needed
    res = g.db.members.find_one({'publicKey': data['publicKey']})
    if not res:
        raise ErrorToClient('No data')
    for key in ['_id', 'signedMessage', 'timestamp', 'twitter']:
        del res[key]
    try:
        res['BDT_balance'] = blank_token_balance(check_eth_addr(res['ethereum_address']))
    except:
        res['BDT_balance'] =  'No Address Founded'
        pass
    res['points'] = calculate_rewards(res['publicKey'])
    # TODO: check bright id confirm
    return json.dumps({'status': True, 'data': res, 'brightid_confirm': True})



@app.route('/submit-ethereum', methods=['POST'])
@jwt_required
def submit_ethereum():
    data = json.loads(request.data)
    if 'publicKey' not in data:
        raise ErrorToClient('Error in connection - No publicKey Founded')
    if 'account' not in data:
        raise ErrorToClient('Error in connection - No Account Founded')
    check_eth_addr(data['account'])
    res = g.db.members.find_one({'publicKey': data['publicKey']})
    if not res:
        raise ErrorToClient('No Public Key Founded')
    g.db.members.update_one({
        '_id': res['_id']
    }, {'$set': {
        'ethereum_address': data['account'],
    }},
    upsert=False)
    return json.dumps({'status': True})


@app.route('/is-login')
@jwt_required
def is_login():
    return json.dumps({'status': True, 'login_status': True, 'msg': 'You are login'})


def calculate_rewards(publicKey):
    res = g.db.points.find({'publicKey': publicKey})
    if res.count() == 0:
        return 0
    points = 0
    for item in res:
        points += item['value']
    return points


def add_brightid_score(publicKey, brightid_level_reached=False, score=0):
    g.db.members.update_one({
        'publicKey': publicKey
    }, {'$set': {
        'score': score,
    }},
    upsert=False)

    if brightid_level_reached:
        return True

    score = True if score >= 90 else False

    # if not score:
    #         return score

    g.db.members.update_one({
        'publicKey': publicKey
    }, {'$set': {
        'brightid_level_reached': score,
    }},
    upsert=False)

    if  not score:
        return False
    g.db.points.insert_one({
        'publicKey': publicKey,
        'type': 'brightid_score',
        'value': config.REWARDS.brightid_score
    })
    return True


def init_types(data):
    data['points'] = 0
    data['credit'] = 0
    data['earned'] = 0
    data['instagram'] = None
    data['instagram_confirmation'] = False
    data['twitter'] = None
    data['twitter_confirmation'] = False
    # data['brightid_level_reached'] = False
    return data


def jwt_create_token(publicKey):
    # Create our JWTs
    access_token = create_access_token(identity=publicKey)
    refresh_token = create_refresh_token(identity=publicKey)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

    ret = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return ret

@app.route('/login', methods=['POST'])
def submit_member():
    # TODO: just allow the js server call this function - get a signutare
    data = json.loads(request.data)

    if not verify_message(data['publicKey'], data['timestamp'],
                          data['signedMessage']):
        raise ErrorToClient('Invalid Data')

    res = g.db.members.find_one({'publicKey': data['publicKey']})
    r = { 'status': True, 'publicKey': data['publicKey'] }
    if res:
        add_brightid_score(data['publicKey'], res['brightid_level_reached'], data['score'])
        token = jwt_create_token(data['publicKey'])
        r.update( token )
        return jsonify( r ), 201

    data = init_types(data)
    g.db.members.insert_one(data)
    add_brightid_score(data['publicKey'], False, data['score'])
    token = jwt_create_token(data['publicKey'])
    r.update( token )
    return jsonify( r ), 201


@app.route('/logout')
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
    return json.dumps({'status': True, 'msg': 'Logout Successfully'})


@app.route('/new-code')
def new_code():
    try:
        r = requests.get('http://127.0.0.1:2200/new-code')
        return r.text
    except Exception as e:
        raise ErrorToClient('Cant Get New Connection')


@app.route('/check-code', methods=['POST'])
def check_code():
    data = json.loads(request.data)
    r = requests.post('http://127.0.0.1:2200/check-code', data=data)
    return r.text


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
@jwt_required
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
        'status': True
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
    g.db.points.insert_one({
        'publicKey': res['publicKey'],
        'type': 'twitter',
        'value': config.REWARDS.twitter
    })
    return redirect('/index.html')



@app.route('/instagram-image', methods = ['POST'])
def instagram_image():
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


# user allow us to check her/his account for new post
@app.route('/instagram-apply', methods = ['POST'])
def instagram_apply():
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
    g.blank_token_contract = g.w3.eth.contract(
            address=config.BLANK_TOKEN_ADDR, abi=config.BLANK_TOKEN_ABI)

    func = g.blank_token_contract.functions.balanceOf(account)
    result = func.call({'from': account})
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008, threaded=True)
