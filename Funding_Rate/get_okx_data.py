'''
Author: Zih0206
'''

import json
import requests
from datetime import datetime
import hmac
import hashlib
import base64
from urllib.parse import urlencode
from enum import Enum
import pandas as pd
import time

class Side(Enum):
    BUY = 'Buy'
    SELL = 'SELL'


class OrderType(Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'
    STOP_MARKET = 'STOP_MARKET'
    TAKE_PROFIT = 'TAKE_PROFIT'
    TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    TRAILING_STOP_MARKET = 'TRAILING_STOP_MARKET'


class TimeInForce(Enum):
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'
    GTX = 'GTX'

class RequestMethod(Enum):
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    PUT = 'put'
class Okx_data(object):
    def __init__(self, base_url= None, api_key= None, api_secret= None, passphrase=None, timeout = 5):

        self.base_url = base_url if base_url else 'https://www.okx.com'
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = passphrase
        self.timeout = timeout

    def sign(self, method, path, query_params = None, request_body = None):
        timestamp = self.get_timestamp()
        if query_params:
            path = path + "?" + urlencode(query_params)
        if request_body:
            data = json.dump(request_body)
            msg = timestamp + method + path + data
        else:
            msg = timestamp + method + path
        digest = hmac.new(self.api_secret.encode('utf-8'), msg.encode('utf-8'),digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode('utf-8')

        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.api_passphrase,
            'Content-Type': 'application/json'
        }

        return headers


    def _build_params(self, params:dict):
        requery = '&'.join([f"{key}={params[key]}" for key in params.keys()])
        return requery

    def get_timestamp(self):
        now = datetime.utcnow()
        timestamp = now.isoformat('T', 'milliseconds')
        return timestamp + 'Z'

    def get_instrument_info(self, instType, uly=None, instFamily=None, instId=None):
        path = '/api/v5/public/instruments'
        params = {'instType': instType}
        url = self.base_url + path
        print(url)
        response = requests.get(url, params=params, timeout=self.timeout).json()
        return response
        
    
    def get_his_fundingRate(self, instid, before=None, after=None, limit=100):
        path = '/api/v5/public/funding-rate-history'
        
        params = {'instId': instid,
            "limit": limit}
        
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        
        url = self.base_url + path
        
        response_data = requests.get(url, params=params, timeout=self.timeout).json()
        return response_data

    def get_account_balance(self, ccy=None):
        path = '/api/v5/account/balance'
        params = {}
        if ccy:
            params['ccy'] = ccy

        headers = self.sign('GET', path)
        url = self.base_url + path
        response_data = requests.get(url, headers=headers, params=params, timeout=self.timeout).json()
        return response_data
