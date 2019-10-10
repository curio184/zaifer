import hashlib
import hmac
import json
import time
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlencode

import requests

from zaifer.zaifapi.exception import *


class HttpConnection():
    '''
    ZaifAPIへの接続を表します。
    '''

    def __init__(self, base_url: str = None, key: str = None, secret: str = None):
        '''
        コンストラクタ
        '''
        self._base_url = base_url
        self._key = key
        self._secret = secret

    def post(self, method: str, params: dict) -> dict:
        '''
        POST要求を送信します。
        '''
        # 引数を検証
        method = '' if method is None else method
        params = {} if params is None else params

        # POST要求を作成
        url = self._base_url + method

        # 認証情報を作成
        encoded_params = urlencode(params)
        http_headers = self._create_http_headers(encoded_params)

        # POST要求を送信
        response = requests.post(
            url, data=encoded_params, headers=http_headers)

        # レスポンスを取得
        if response.status_code != 200:
            raise Exception(
                'return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def get(self, method: str, params: dict) -> dict:
        '''
        GET要求を送信します。
        '''
        # 引数を検証
        method = '' if method is None else method
        params = {} if params is None else params

        # GET要求を作成
        url = self._base_url + method

        # GET要求を送信
        response = requests.get(url, params=params)

        # レスポンスを取得
        if response.status_code != 200:
            raise Exception(
                'return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def _create_http_headers(self, params: str) -> dict:
        '''
        HTTPヘッダーを作成します。
        '''
        return self._create_signature(self._key, self._secret, params)

    def _create_signature(self, key: str, secret: str, params: str) -> dict:
        '''
        デジタル署名を作成します。
        '''
        signature = hmac.new(
            bytearray(secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(params.encode('utf-8'))
        return {
            'key': key,
            'sign': signature.hexdigest()
        }


class UrlConfigs():
    '''
    ZaifAPIの接続情報を表します。
    '''

    def __init__(self):

        self._public_api_url = 'https://api.zaif.jp/api/1'
        self._trade_api_url = 'https://api.zaif.jp/tapi'
        self._margin_public_api_url = 'https://api.zaif.jp/fapi/1'
        self._margin_trade_api_url = 'https://api.zaif.jp/tlapi'
        self._chart_api_url = 'https://zaif.jp/zaif_chart_api/v1'

    @property
    def public_api_url(self) -> str:
        return self._public_api_url

    @public_api_url.setter
    def public_api_url(self, value: str):
        self._public_api_url = value

    @property
    def trade_api_url(self) -> str:
        return self._trade_api_url

    @trade_api_url.setter
    def trade_api_url(self, value: str):
        self._trade_api_url = value

    @property
    def margin_public_api_url(self) -> str:
        return self._margin_public_api_url

    @margin_public_api_url.setter
    def margin_public_api_url(self, value: str):
        self._margin_public_api_url = value

    @property
    def margin_trade_api_url(self) -> str:
        return self._margin_trade_api_url

    @margin_trade_api_url.setter
    def margin_trade_api_url(self, value: str):
        self._margin_trade_api_url = value

    @property
    def chart_api_url(self) -> str:
        return self._chart_api_url

    @chart_api_url.setter
    def chart_api_url(self, value: str):
        self._chart_api_url = value


class NonceGenerator():
    '''
    ノンスを生成します。
    '''

    @staticmethod
    def generate() -> Decimal:
        '''
        ノンスを生成します。
        '''
        now = datetime.now()
        datetime_part = str(int(time.mktime(now.timetuple())))
        second_part = '{0:06d}'.format(now.microsecond)

        return Decimal(datetime_part + '.' + second_part)


class ResponseParser():
    '''
    レスポンスをパースします。
    '''

    @staticmethod
    def parse(response: dict) -> dict:
        '''
        レスポンスをパースします。
        '''
        if response['success'] == 0:
            if response['error'] == 'no data found for the key':
                raise InvalidAPIKeyException(response['error'])
            elif response['error'] == 'signature mismatch':
                raise InvalidAPISecretException(response['error'])
            elif response['error'] == 'order not found':
                raise OrderNotFoundException(response['error'])
            elif response['error'] == 'nonce not incremented':
                raise NonceNotIcreasedException(response['error'])
            elif response['error'] == 'nonce out of range':
                raise NonceOutOfRangeException(response['error'])
            elif response['error'] == 'trade temporarily unavailable.':
                raise TradeTemporarilyUnavailableException(response['error'])
            elif response['error'] == 'invalid amount parameter':
                raise InvalidAmountException(response['error'])
            elif response['error'] == 'time out':
                raise TimeoutException(response['error'])
            raise Exception(response['error'])

        return response['return']
