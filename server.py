#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, g, session
from web3 import Web3, HTTPProvider
from io import BytesIO as IO
from datetime import timedelta
from eth_keys import keys
import functools
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
    if (response.status_code < 200 or
        response.status_code >= 300 or
        'Content-Encoding' in response.headers):
        return response
    gzip_buffer = IO()
    gzip_file = gzip.GzipFile(mode='wb',
                              fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)
    return response


@app.errorhandler(ErrorToClient)
def error_to_client(error):
    return json.dumps({'msg': error.args[0], 'args': error.args[1:], 'status': False})


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


@app.after_request
def after_request(response):
    return gzip_content(response)


@app.teardown_request
def teardown_request(exception):
    pass


def allow_child(db, child):
    mydoc = db.find_one({"child": child})
    print(mydoc)
    # import pdb
    # pdb.set_trace()
    if mydoc:
        if mydoc['registered'] == False:
            return mydoc
    return False


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.route('/check-account', methods=['POST'])
def check_account():
    data = json.loads(request.data)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["blankdao"]
    mycol = mydb["referrers"]
    w3 = Web3(HTTPProvider(config.INFURA_URL))
    res = allow_child(mycol, w3.toChecksumAddress(data['account']))
    if res:
        if res['registered'] == True:
            raise ErrorToClient('Your account has already been registered', {'referrer': res['parent']})
    return json.dumps({'status': True, 'msg': 'Allow'})


@app.route('/add-referrer', methods=['POST'])
def add_referrer():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["blankdao"]
    mycol = mydb["referrers"]

    w3 = Web3(HTTPProvider(config.INFURA_URL))
    data = json.loads(request.data)

    try:
        parent = w3.toChecksumAddress(data['parent'])
        child = w3.toChecksumAddress(data['child'])
    except Exception as e:
        print(e)
        raise ErrorToClient('Your Account Addresses Not Correct')
    res = allow_child(mycol, child)
    if res:
        if res['registered'] == True:
            raise ErrorToClient('Your account has already been registered')
        else:
            mycol.update_one({
              '_id': res['_id']
            },{
              '$set': {
                'parent': parent
              }
            }, upsert=False)
    mycol.insert_one({"parent": parent, "child": child, "registered": False})
    return json.dumps({'msg':'Your Address Submied Successfully', 'status': True})


def priv2addr(private_key):
    pk = keys.PrivateKey(bytes.fromhex(private_key))
    return pk.public_key.to_checksum_address()


def send_eth_call(func, sender):
    result = func.call({
        'from': sender,
    })
    return result


def send_transaction(func, value, private_key):
    transaction = func.buildTransaction({
        'nonce':
        w3.eth.getTransactionCount(priv2addr(private_key)),
        'from':
        priv2addr(private_key),
        'value':
        value,
        'gas':
        config.GAS,
        'gasPrice':
        config.GAS_PRICE
    })
    signed = w3.eth.account.signTransaction(transaction, private_key)
    raw_transaction = signed.rawTransaction.hex()
    tx_hash = w3.eth.sendRawTransaction(raw_transaction).hex()
    rec = w3.eth.waitForTransactionReceipt(tx_hash)
    if rec['status']:
        print('tx: {}'.format(tx_hash))
    else:
        print('Reverted!\nError occured during contract execution')
    print()
    return tx_hash



if __name__ == '__main__':
    app.run(debug=True, port=5008, threaded=True)
