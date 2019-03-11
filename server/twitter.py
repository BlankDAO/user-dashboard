from requests_oauthlib import OAuth1Session
from config import TWIITER_API as config
from time import time as now
from flask import g


def twitter_get_oauth_request_token(publicKey):
    twitter_url = 'https://api.twitter.com/oauth'
    request_token = OAuth1Session(client_key=config['consumer_key'], client_secret=config['consumer_secret'])
    url = twitter_url + '/request_token'
    data = request_token.get(url)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    g.db.twitter_temp.update_one({
        'publicKey': publicKey
        }, {'$set': {
            'resource_owner_key': resource_owner_key,
            'resource_owner_secret': resource_owner_secret,
            'time': now(),
        }},upsert=True)
    return '{}/authenticate?oauth_token={}'.format(twitter_url, resource_owner_key)


def twitter_get_oauth_token(verifier, ro_key, ro_secret):
    oauth_token = OAuth1Session(client_key=config['consumer_key'],
                                client_secret=config['consumer_secret'],
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": verifier}
    access_token_data = oauth_token.post(url, data=data)
    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list


def twitter_get_access_token(access_token_list):
    access_token_key = str.split(access_token_list[0], '=')
    access_token_secret = str.split(access_token_list[1], '=')
    access_token_name = str.split(access_token_list[3], '=')
    access_token_id = str.split(access_token_list[2], '=')
    key = access_token_key[1]
    secret = access_token_secret[1]
    name = access_token_name[1]
    id = access_token_id[1]
    oauth_user = OAuth1Session(client_key=config['consumer_key'],
                               client_secret=config['consumer_secret'],
                               resource_owner_key=key,
                               resource_owner_secret=secret)
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    params = {"include_email": 'true'}
    user_data = oauth_user.get(url_user, params=params)
    return user_data.json()
