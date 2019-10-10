import json
import time
from datetime import datetime
from decimal import Decimal

from zaifer.zaifapi.connection import (HttpConnection, NonceGenerator,
                                       ResponseParser, UrlConfigs)
from zaifer.zaifapi.utils import NumericConverter


class Chart():
    '''
    チャート情報を取得します。
    '''

    def __init__(self, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(url_config.chart_api_url)

    def get_ohlc(self, currency_pair: str, period: str, from_datetime: datetime, to_datetime: datetime) -> dict:
        '''
        チャート情報を取得します。
        period :
            1分足:1、5分足:5、15分足:15、30分足:30、1時間足:60、4時間足:240、8時間足:480、12時間足:720、1日足:D、1週足:W
        '''
        params = {
            'symbol': currency_pair,
            'resolution': period,
            'from': str(int(time.mktime(from_datetime.timetuple()))),
            'to': str(int(time.mktime(to_datetime.timetuple())))
        }
        res = self._connection.get('/history', params)
        # NOTE:取得に成功した場合、なぜか2度エンコードされているのでデコードも2度する
        if isinstance(res, str):
            return json.loads(res)
        else:
            return res


class Account():
    '''
    アカウント情報を取得します。

    対応ドキュメント：現物取引API
    https://zaif-api-document.readthedocs.io/ja/latest/TradingAPI.html
    '''

    def __init__(self, key, secret, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(url_config.trade_api_url, key, secret)

    def get_info(self) -> dict:
        '''
        残高情報を取得します。
        '''
        params = {
            'method': 'get_info',
            'nonce': NonceGenerator.generate()
        }
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_info2(self) -> dict:
        '''
        残高情報を取得します。(軽量版)
        '''
        params = {
            'method': 'get_info2',
            'nonce': NonceGenerator.generate()
        }
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_personal_info(self) -> dict:
        '''
        チャット情報を取得します。
        '''
        params = {
            'method': 'get_personal_info',
            'nonce': NonceGenerator.generate()
        }
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_id_info(self) -> dict:
        '''
        アカウント情報を取得します。
        '''
        params = {
            'method': 'get_id_info',
            'nonce': NonceGenerator.generate()
        }
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def withdraw(self, currency: str, address: str, amount: Decimal,
                 message: str = None, opt_fee: Decimal = None) -> dict:
        '''
        出金を依頼します。
        '''
        params = {
            'method': 'withdraw',
            'nonce': NonceGenerator.generate(),
            'currency': currency,
            'address': address,
            'amount': amount
        }
        if message is not None:
            params['message'] = message
        if opt_fee is not None:
            params['opt_fee'] = opt_fee
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_deposit_history(self, currency: str, since: datetime = None, end: datetime = None,
                            _from: int = None, count: int = None,
                            from_id: int = None, end_id: int = None, order: str = None) -> dict:
        '''
        入金履歴を取得します。
        '''
        params = {
            'method': 'deposit_history',
            'nonce': NonceGenerator.generate(),
            'currency': currency
        }
        if _from is not None:
            params['from'] = str(_from)
        if count is not None:
            params['count'] = str(count)
        if from_id is not None:
            params['from_id'] = str(from_id)
        if end_id is not None:
            params['end_id'] = str(end_id)
        if order is not None:
            params['order'] = order
        if since is not None:
            params['since'] = str(int(time.mktime(since.timetuple())))
        if end is not None:
            params['end'] = str(int(time.mktime(end.timetuple())))
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_withdraw_history(self, currency: str, since: datetime = None, end: datetime = None,
                             _from: int = None, count: int = None,
                             from_id: int = None, end_id: int = None, order: str = None) -> dict:
        '''
        出金履歴を取得します。
        '''
        params = {
            'method': 'withdraw_history',
            'nonce': NonceGenerator.generate(),
            'currency': currency
        }
        if _from is not None:
            params['from'] = str(_from)
        if count is not None:
            params['count'] = str(count)
        if from_id is not None:
            params['from_id'] = str(from_id)
        if end_id is not None:
            params['end_id'] = str(end_id)
        if order is not None:
            params['order'] = order
        if since is not None:
            params['since'] = str(int(time.mktime(since.timetuple())))
        if end is not None:
            params['end'] = str(int(time.mktime(end.timetuple())))
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)


class Market():
    '''
    現物取引のマーケット情報を取得します。

    対応ドキュメント：現物公開API
    https://zaif-api-document.readthedocs.io/ja/latest/PublicAPI.html
    '''

    def __init__(self, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(url_config.public_api_url)

    def get_currencies(self, currency: str) -> dict:
        '''
        通貨情報を取得します。
        '''
        return self._connection.get('/currencies/{}'.format(currency), None)

    def get_currency_pairs(self, currency_pair: str) -> dict:
        '''
        通貨ペア情報を取得します。
        '''
        return self._connection.get('/currency_pairs/{}'.format(currency_pair), None)

    def get_last_price(self, currency_pair: str) -> dict:
        '''
        現在の終値を取得します。
        '''
        return self._connection.get('/last_price/{}'.format(currency_pair), None)

    def get_ticker(self, currency_pair: str) -> dict:
        '''
        ティッカーを取得します。
        '''
        return self._connection.get('/ticker/{}'.format(currency_pair), None)

    def get_trade_history(self, currency_pair: str) -> dict:
        '''
        全ユーザーの取引履歴を取得します。
        '''
        return self._connection.get('/trades/{}'.format(currency_pair), None)

    def get_depth(self, currency_pair: str) -> dict:
        '''
        板情報を取得します。
        '''
        return self._connection.get('/depth/{}'.format(currency_pair), None)


class Trade():
    '''
    現物取引の注文情報を取得・送信します。

    対応ドキュメント：現物取引API
    https://zaif-api-document.readthedocs.io/ja/latest/TradingAPI.html
    '''

    def __init__(self, key, secret, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(url_config.trade_api_url, key, secret)

    def get_trade_history(self, currency_pair: str = None, since: datetime = None, end: datetime = None,
                          _from: int = None, count: int = None,
                          from_id: int = None, end_id: int = None,
                          order: str = None, is_token: bool = None) -> dict:
        '''
        ユーザー自身の取引履歴を取得します。
        '''
        params = {
            'method': 'trade_history',
            'nonce': NonceGenerator.generate()
        }
        if _from is not None:
            params['from'] = str(_from)
        if count is not None:
            params['count'] = str(count)
        if from_id is not None:
            params['from_id'] = str(from_id)
        if end_id is not None:
            params['end_id'] = str(end_id)
        if order is not None:
            params['order'] = order
        if since is not None:
            params['since'] = str(int(time.mktime(since.timetuple())))
        if end is not None:
            params['end'] = str(int(time.mktime(end.timetuple())))
        if currency_pair is not None:
            params['currency_pair'] = currency_pair
        if is_token is not None:
            params['is_token'] = is_token
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_active_orders(self, currency_pair: str = None, is_token: bool = None, is_token_both: bool = None) -> dict:
        '''
        現在有効な注文一覧を取得します（未約定注文一覧）。
        '''
        params = {
            'method': 'active_orders',
            'nonce': NonceGenerator.generate()
        }
        if currency_pair is not None:
            params['currency_pair'] = currency_pair
        if is_token is not None:
            params['is_token'] = str(is_token)
        if is_token_both is not None:
            params['is_token_both'] = str(is_token_both)
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def open_order(self, currency_pair: str, action: str, price: Decimal, amount: Decimal, limit: Decimal = None, comment: str = None) -> dict:
        '''
        新規注文を送信します。
        '''
        params = {
            'method': 'trade',
            'nonce': NonceGenerator.generate(),
            'currency_pair': currency_pair,
            'action': action,
            'price': NumericConverter.decimal_to_str(price),
            'amount': NumericConverter.decimal_to_str(amount)
        }
        if limit is not None:
            params['limit'] = limit
        if comment is not None:
            params['comment'] = comment
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def cancel_order(self, order_id: int, currency_pair: str = None, is_token: bool = None) -> dict:
        '''
        キャンセル注文を送信します。
        '''
        params = {
            'method': 'cancel_order',
            'nonce': NonceGenerator.generate(),
            'order_id': order_id
        }
        if currency_pair is not None:
            params['currency_pair'] = currency_pair
        if is_token is not None:
            params['is_token'] = is_token
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)


class MarginMarket():
    '''
    証拠金取引(信用取引およびAirFX)のマーケット情報を取得します。

    対応ドキュメント：なし
    '''

    def __init__(self, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(url_config.margin_public_api_url)

    def get_groups(self, group_id: str) -> dict:
        """
        先物取引のグループIDを取得します。

        Parameters
        ----------
        group_id : str
            数字を指定した場合、対応するグループIDのみを取得します。
            'all'を指定した場合、取引が終了したものを含むすべてのグループIDを取得します。
            'active'を指定した場合、現在取引可能なグループIDのみを取得します。
        """
        return self._connection.get('/groups/{}'.format(str(group_id)), None)

    def get_last_price(self, group_id: int, currency_pair: str) -> dict:
        '''
        現在の終値を取得します。
        '''
        return self._connection.get('/last_price/{}/{}'.format(str(group_id), currency_pair), None)

    def get_ticker(self, group_id: int, currency_pair: str) -> dict:
        '''
        ティッカーを取得します。
        '''
        return self._connection.get('/ticker/{}/{}'.format(str(group_id), currency_pair), None)

    def get_trade_history(self, group_id: int, currency_pair: str) -> dict:
        '''
        全ユーザの取引履歴を取得します。
        '''
        return self._connection.get('/trades/{}/{}'.format(str(group_id), currency_pair), None)

    def get_depth(self, group_id: int, currency_pair: str) -> dict:
        '''
        板情報を取得します。
        '''
        return self._connection.get('/depth/{}/{}'.format(str(group_id), currency_pair), None)

    def get_swap_history(self, group_id: int, currency_pair: str) -> dict:
        '''
        確定したスワップポイントの履歴を取得します。
        '''
        return self._connection.get('/swap_history/{}/{}'.format(str(group_id), currency_pair), None)


class MarginTrade():
    '''
    証拠金取引(信用取引およびAirFX)の注文情報を取得・送信します。

    対応ドキュメント：信用取引API, AirFXAPI
    https://zaif-api-document.readthedocs.io/ja/latest/MarginTradingAPI.html
    https://zaif-api-document.readthedocs.io/ja/latest/AirFXAPI.html
    '''

    def __init__(self, key, secret, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._connection = HttpConnection(
            url_config.margin_trade_api_url, key, secret)

    def get_positions(self, _type: str, group_id: int = None, currency_pair: str = None,
                      since: datetime = None, end: datetime = None, _from: int = None, count: int = None,
                      from_id: int = None, end_id: int = None, order: str = None) -> dict:
        """
        証拠金取引のユーザー自身の取引履歴を取得します。
        """

        params = {
            'method': 'get_positions',
            'nonce': NonceGenerator.generate(),
            'type': _type,
        }
        if group_id is not None:
            params['group_id'] = group_id
        if _from is not None:
            params['from'] = str(_from)
        if count is not None:
            params['count'] = str(count)
        if from_id is not None:
            params['from_id'] = str(from_id)
        if end_id is not None:
            params['end_id'] = str(end_id)
        if order is not None:
            params['order'] = order
        if since is not None:
            params['since'] = str(int(time.mktime(since.timetuple())))
        if end is not None:
            params['end'] = str(int(time.mktime(end.timetuple())))
        if currency_pair is not None:
            params['currency_pair'] = currency_pair
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_position_history(self, _type: str, group_id: int, order_id: int) -> dict:
        '''
        証拠金取引のユーザー自身の取引履歴の明細を取得します。
        '''
        params = {
            'method': 'position_history',
            'nonce': NonceGenerator.generate(),
            'type': _type,
            'leverage_id': order_id
        }
        if group_id is not None:
            params['group_id'] = group_id
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def get_active_positions(self, _type: str, group_id: int = None, currency_pair: str = None) -> dict:
        '''
        証拠金取引の現在有効な注文一覧を取得します（未約定注文一覧）。
        '''
        params = {
            'method': 'active_positions',
            'nonce': NonceGenerator.generate(),
            'type': _type
        }
        if group_id is not None:
            params['group_id'] = group_id
        if currency_pair is not None:
            params['currency_pair'] = currency_pair
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def create_position(self, _type: str, group_id: int, currency_pair: str, action: str, price: Decimal, amount: Decimal, leverage: Decimal, limit: Decimal = None, stop: Decimal = None) -> dict:
        '''
        証拠金取引の新規注文を送信します。
        '''
        params = {
            'method': 'create_position',
            'nonce': NonceGenerator.generate(),
            'type': _type,
            'currency_pair': currency_pair,
            'action': action,
            'price': price,
            'amount': amount,
            'leverage': leverage
        }
        if group_id is not None:
            params['group_id'] = group_id
        if limit is not None:
            params['limit'] = limit
        if stop is not None:
            params['stop'] = stop
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def update_position(self, _type: str, group_id: int, order_id: int, price: Decimal, limit: Decimal = None, stop: Decimal = None) -> dict:
        '''
        証拠金取引の修正注文を送信します。
        '''
        params = {
            'method': 'change_position',
            'nonce': NonceGenerator.generate(),
            'type': _type,
            'leverage_id': order_id,
            'price': price,
        }
        if group_id is not None:
            params['group_id'] = group_id
        if limit is not None:
            params['limit'] = limit
        if stop is not None:
            params['stop'] = stop
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)

    def cancel_position(self, _type: str, group_id: int, order_id: int) -> dict:
        '''
        証拠金取引のキャンセル注文を送信します。
        '''
        params = {
            'method': 'cancel_position',
            'nonce': NonceGenerator.generate(),
            'type': _type,
            'leverage_id': order_id
        }
        if group_id is not None:
            params['group_id'] = group_id
        res = self._connection.post(None, params)
        return ResponseParser.parse(res)


class AirFXMarket():
    '''
    AirFXのマーケット情報を取得します。

    対応ドキュメント：なし
    '''

    def __init__(self, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._group_id = 1
        self._currency_pair = "btc_jpy"
        self._margin_market = MarginMarket(url_config)

    def get_last_price(self) -> dict:
        '''
        現在の終値を取得します。
        '''
        return self._margin_market.get_last_price(
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )

    def get_ticker(self) -> dict:
        '''
        ティッカーを取得します。
        '''
        return self._margin_market.get_ticker(
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )

    def get_trade_history(self) -> dict:
        '''
        全ユーザの取引履歴を取得します。
        '''
        return self._margin_market.get_trade_history(
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )

    def get_depth(self) -> dict:
        '''
        板情報を取得します。
        '''
        return self._margin_market.get_depth(
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )

    def get_swap_history(self) -> dict:
        '''
        確定したスワップポイントの履歴を取得します。
        '''
        return self._margin_market.get_swap_history(
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )


class AirFXTrade():
    '''
    AirFXの注文情報を取得・送信します。

    対応ドキュメント：AirFXAPI
    https://zaif-api-document.readthedocs.io/ja/latest/AirFXAPI.html
    '''

    def __init__(self, key, secret, url_config: UrlConfigs = UrlConfigs()):
        '''
        コンストラクタ
        '''
        self._type = "futures"
        self._group_id = 1
        self._currency_pair = "btc_jpy"
        self._margin_trade = MarginTrade(key, secret, url_config)

    def get_positions(self, since: datetime = None, end: datetime = None,
                      _from: int = None, count: int = None,
                      from_id: int = None, end_id: int = None, order: str = None) -> dict:
        '''
        証拠金取引のユーザー自身の取引履歴を取得します。
        '''
        return self._margin_trade.get_positions(
            _type=self._type,
            group_id=self._group_id,
            currency_pair=self._currency_pair,
            since=since,
            end=end,
            _from=_from,
            count=count,
            from_id=from_id,
            end_id=end_id,
            order=order
        )

    def get_position_history(self, order_id: int) -> dict:
        '''
        証拠金取引のユーザー自身の取引履歴の明細を取得します。
        '''
        return self._margin_trade.get_position_history(
            _type=self._type,
            group_id=self._group_id,
            order_id=order_id
        )

    def get_active_positions(self) -> dict:
        '''
        証拠金取引の現在有効な注文一覧を取得します（未約定注文一覧）。
        '''
        return self._margin_trade.get_active_positions(
            _type=self._type,
            group_id=self._group_id,
            currency_pair=self._currency_pair
        )

    def create_position(self, action: str, price: Decimal, amount: Decimal, leverage: Decimal, limit: Decimal = None, stop: Decimal = None) -> dict:
        '''
        証拠金取引の新規注文を送信します。
        '''
        return self._margin_trade.create_position(
            _type=self._type,
            group_id=self._group_id,
            currency_pair=self._currency_pair,
            action=action,
            price=price,
            amount=amount,
            leverage=leverage,
            limit=limit,
            stop=stop
        )

    def update_position(self, order_id: int, price: Decimal, limit: Decimal = None, stop: Decimal = None) -> dict:
        '''
        証拠金取引の修正注文を送信します。
        '''
        return self._margin_trade.update_position(
            _type=self._type,
            group_id=self._group_id,
            order_id=order_id,
            price=price,
            limit=limit,
            stop=stop
        )

    def cancel_position(self, order_id: int) -> dict:
        '''
        証拠金取引のキャンセル注文を送信します。
        '''
        return self._margin_trade.cancel_position(
            _type=self._type,
            group_id=self._group_id,
            order_id=order_id
        )
