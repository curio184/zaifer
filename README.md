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


# Zaifのアカウント画面で取得したAPIキーを設定します。
key = 'aa75ffcc-6c72-4b54-a936-xxxxxxxxxxxx'
secret = '0fbe7367-0821-4417-9c65-xxxxxxxxxxxx'

# アカウント情報を取得します。
account = Account(key, secret)
print(account.get_info())
print(account.get_info2())
print(account.get_personal_info())
print(account.get_id_info())
print(account.withdraw('btc', '17A16QmavnUfCW11DAApiJxp7ARxxxxxxxx', Decimal('10.0'), None, Decimal('0.0005')))
print(account.get_deposit_history('jpy'))
print(account.get_withdraw_history('btc'))

# チャート情報を取得します。
chart = Chart()
print(chart.get_ohlc('btc_jpy', '60', datetime(
        2018, 11, 4, 0), datetime(2018, 11, 5, 0)))

# 現物取引のマーケット情報を取得します。
market = Market()
print(market.get_currencies('all'))
print(market.get_currency_pairs('btc_jpy'))
print(market.get_last_price('btc_jpy'))
print(market.get_ticker('btc_jpy'))
print(market.get_trade_history('btc_jpy'))
print(market.get_depth('btc_jpy'))

# 現物取引の注文情報を取得・送信します。
trade = Trade(key, secret)
print(trade.get_trade_history('btc_jpy', datetime(2018, 11, 5)))
print(trade.get_active_orders())
print(trade.open_order('btc_jpy', 'bid', Decimal('780000'), Decimal('1')))
print(trade.cancel_order(92537563))

# AirFXのマーケット情報を取得します。
airfx_market = AirFXMarket()
print(airfx_market.get_last_price())
print(airfx_market.get_ticker())
print(airfx_market.get_trade_history())
print(airfx_market.get_depth())
print(airfx_market.get_swap_history())

# AirFXの注文情報を取得・送信します。
airfx_trade = AirFXTrade(key, secret)
print(airfx_trade.get_positions())
print(airfx_trade.get_position_history(2864))
print(airfx_trade.get_active_positions())
print(airfx_trade.create_position('bid', 420100, 1, 4))
print(airfx_trade.update_position(22904, 720000))
print(airfx_trade.cancel_position(22905))
```

関連情報
-------------
* [ZaifAPIドキュメント](https://zaif-api-document.readthedocs.io/ja/latest/)
 
