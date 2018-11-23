zaifer
=============
![](https://img.shields.io/apm/l/vim-mode.svg)
![](https://img.shields.io/badge/Python-after%20v3-red.svg)
[![](https://img.shields.io/pypi/v/zaifer.svg)](https://pypi.org/project/zaifer/)

zaiferとは、zaifapiのラッパーライブラリです。
webapiを利用するための煩雑な手続きを隠蔽し、
zaifapiをpythonのmethodベースで簡単に利用できます。

使い方
-------------
１．ZaifのアカウントページでAPIKeyを発行します。

```
APIKeyは第３者に明かさないよう大切に扱ってください。
```

２．pipコマンドを実行し、モジュールをダウンロードしてください。

```
pip install zaifer
```

３．クラスをインポートし、下記の通り使用してください。

```python
from datetime import datetime
from decimal import Decimal

from zaifer import *


# APIキーを設定
key = 'aa75ffcc-6c72-4b54-a936-xxxxxxxxxxxx'
secret = '0fbe7367-0821-4417-9c65-xxxxxxxxxxxx'

# アカウント情報を取得します。
account = Account(key, secret)
print(account.get_info())
print(account.get_info2())
print(account.get_personal_info())
print(account.get_id_info())
print(account.withdraw('btc', '17A16QmavnUfCW11DAApiJxp7ARxxxxxxxx', Decimal('10.0'), None, Decimal('0.0005')))
print(account.get_deposit_history_by_period('jpy'))
print(account.get_withdraw_history_by_period('btc'))

# 現物取引のマーケット情報を取得します。
market = Market()
print(market.get_currencies('all'))
print(market.get_currency_pairs('btc_jpy'))
print(market.get_last_price('btc_jpy'))
print(market.get_ticker('btc_jpy'))
print(market.get_trade_history('btc_jpy'))
print(market.get_depth('btc_jpy'))

# チャート情報を取得します。
chart = Chart()
print(chart.get_ohlc('btc_jpy', '60', datetime(
        2018, 11, 4, 0), datetime(2018, 11, 5, 0)))

# 現物取引の注文情報を取得・送信します。
trade = Trade(key, secret)
print(trade.get_trade_history_by_period(
    'btc_jpy', datetime(2018, 11, 5)))
print(trade.get_active_orders())
print(trade.open_order('btc_jpy', 'bid', Decimal('780000'), Decimal('1')))
print(trade.cancel_order(92537563))

# 先物取引のマーケット情報を取得します。
futureMarket = FutureMarket()
print(futureMarket.get_groups('active'))
print(futureMarket.get_last_price(1, 'btc_jpy'))
print(futureMarket.get_ticker(1, 'btc_jpy'))
print(futureMarket.get_trade_history(1, 'btc_jpy'))
print(futureMarket.get_depth(1, 'btc_jpy'))
print(futureMarket.get_swap_history(1, 'btc_jpy'))

# 証拠金取引の注文情報を取得・送信します。
marginTrade = MarginTrade(key, secret)

# BTC/JPYの信用取引
print(marginTrade.get_positions('margin', None, 'btc_jpy'))
print(marginTrade.position_history('margin', None, 22701))
print(marginTrade.get_active_positions('margin', None))
print(marginTrade.create_position('margin', None, 'btc_jpy', 'bid', 721000, 1, 7.77))
print(marginTrade.update_position('margin', None, 22904, 720000))
print(marginTrade.cancel_position('margin', None, 22905))

# BTC/JPYの先物取引(AirFX)
print(marginTrade.get_positions('futures', 1, 'btc_jpy'))
print(marginTrade.position_history('futures', 1, 22701))
print(marginTrade.get_active_positions('futures', 1))
print(marginTrade.create_position('futures', 1, 'btc_jpy', 'bid', 750000, 1, 25))
print(marginTrade.update_position('futures', 1, 22904, 720000))
print(marginTrade.cancel_position('futures', 1, 22905))
```

関連情報
-------------
* [ZaifAPIドキュメント](https://techbureau-api-document.readthedocs.io/ja/latest/)
 
