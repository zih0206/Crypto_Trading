'''
Author: Zih0206
'''


import requests
import pandas as pd
import numpy as np
import time
from enum import Enum
import hashlib
import hmac


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

class Binance_data(object):
    def __init__(self, api_key=None, api_secret=None, base_url=None, timeout=5):
        self.base_url = base_url if base_url else 'https://fapi.binance.com'
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout

    def build_params(self, params:dict):
        requery = '&'.join([f"{key}={params[key]}" for key in params.keys()])
        return requery
        # requery = ''
        # for key in params.keys():
        #     requery += f"{key}={params[key]}&"
        # requery = requery[0:-1]
        # return requery

    def request(self, method, path, params=None, verify=False):
        url = self.base_url + path
        if params:
            url = url + '?' + self.build_params(params)

        if verify:
            query_str = self.build_params(params)
            signature = hmac.new(self.api_secret.encode('utf-8'), msg=query_str.encode('utf-8'),
                                 digestmod=hashlib.sha256).hexdigest()

            url += '&signature=' + signature

        headers = {"X-MBX-APIKEY": self.api_key}
        return requests.request(method.value, url,headers=headers, timeout=self.timeout).json()

    def get_server_status(self):
        path = '/fapi/v1/ping'
        return self.request(RequestMethod.GET,path)

    def get_exchange_info(self):
        path = '/fapi/v1/exchangeInfo'
        return self.request(RequestMethod.GET, path)


    def get_his_fundingRate(self, symbol=None, start_time=None, end_time=None, limit=100):
        path = '/fapi/v1/fundingRate'
        params = {"limit": limit}
        if symbol:
            params['symbol'] = symbol
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        return self.request(RequestMethod.GET, path, params=params)

    ###priviate api####
    def get_timestamp(self):
        return int(time.time() * 1000)

    def place_new_order(self, symbol, side: Side, type_: OrderType, positionSide=None, timeInForce=TimeInForce.GTC,
                        quantity=None, price=None, stop_price=None, callbackRate=None):
        path = '/fapi/v1/order'
        params = {
            'symbol': symbol,
            'side': side.value,
            'type': type_.value,
            'timestamp': self.get_timestamp(),
            'quantity': quantity
        }
        if positionSide:
            params['positionSide'] = positionSide

        if type_ == OrderType.LIMIT:
            params['timeInForce'] = timeInForce.value
            if price > 0:
                params['price'] = price
            else:
                raise ValueError('price cannot be none')

        if type_ == OrderType.MARKET:
            pass

        if type_ == OrderType.STOP or type_ == OrderType.TAKE_PROFIT:
            if price > 0:
                params['price'] = price
            else:
                raise ValueError('Price cannot be Nan')
            if stop_price > 0:
                params['stopPrice'] = stop_price
            else:
                False

        if type_ == OrderType.STOP_MARKET or type_ == OrderType.TAKE_PROFIT_MARKET:
            if stop_price > 0:
                params['stopPrice'] = stop_price
            else:
                raise ValueError('StopPrice should be a value')

        if type_ == OrderType.TRAILING_STOP_MARKET:
            if callbackRate >= 0.001 and callbackRate <= 0.05:
                params['callbackRate'] = callbackRate

        return self.request(RequestMethod.POST, path, params=params, verify=True)


    def get_order_info(self, symbol, orderId=None, recv_window=5000):
        path = '/fapi/v1/order'
        params = {'symbol': symbol,
                  'recvWindow': recv_window,
                  'timestamp': self.get_timestamp()

                  }
        if orderId:
            params['orderId'] = orderId

        query_str = ''
        for key in params.keys():
            query_str += f'{key}={params[key]}&'
        query_str = query_str[0:-1]
        print(query_str)

        return self.request(RequestMethod.GET, path, params=params, verify=True)
      
    def cancel_order(self, symbol, orderId=None, recv_window=5000):
        path = '/fapi/v1/order'
        params = {'symbol': symbol,
                  'recvWindow': recv_window,
                  'timestamp': self.get_timestamp()

                  }
        if orderId:
            params['orderId'] = orderId

        return self.request(RequestMethod.DELETE, path, params=params, verify=True)
     
    def get_open_order(self, symbol=None, recv=None):
        """
         If the symbol is not sent, orders for all symbols will be returned in an array.
        :param symbol:
        :param recv:
        :return:
        """
        path = '/fapi/v1/openOrders'
        params={
            'timestamp': self.get_timestamp()
        }
        if symbol:
            params['symbol'] = symbol
        if recv:
            params['recvWindow'] = recv

        return self.request(RequestMethod.GET, path, params, verify=True)


    def get_account_info(self, recv=None):
        path= '/fapi/v2/account'
        params = {
            'timestamp': self.get_timestamp()
        }
        if recv:
            params['recvWindow'] = recv

        return self.request(RequestMethod.GET, path=path, params=params, verify=True)

    def get_my_balance(self, recv=None):
        path = '/fapi/v2/balance'
        params = {
            'timestamp': self.get_timestamp()
        }
        if recv:
            params['recvWindow'] = recv

        return self.request(RequestMethod.GET, path=path, params=params, verify=True)

    def get_position_info(self, symbol=None, recv=None):
        path = '/fapi/v2/positionRisk'
        params={
            'timestamp': self.get_timestamp()
        }
        if symbol:
            params['symbol'] = symbol

        if recv:
            params['recvWindow'] = recv

        return self.request(RequestMethod.GET, path=path, params=params, verify=True)


