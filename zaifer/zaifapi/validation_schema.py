# 検証スキーマを定義します。
zaifapi_schema = {
    "Chart": {
        "get_ohlc": {
            "currency_pair": {"type":  "string"},
            "period": {"type": "string"},
            "since": {"type": "datetime"},
            "end": {"type": "datetime"},
        },
    },
    "Account": {
        "get_info": {},
        "get_info2": {},
        "get_personal_info": {},
        "get_id_info": {},
        "withdraw": {},
        "get_deposit_history_by_period": {},
        "get_withdraw_history_by_period": {},
    },
    "Market": {
        "get_currencies": {},
        "get_currency_pairs": {},
        "get_lastprice": {
            "currency": {"type":  "string"}
        },
        "get_ticker": {},
        "get_trade_history": {},
        "get_depth": {},
    },
    "Trade": {
        "get_trade_history_by_period": {},
        "get_active_orders": {},
        "open_order": {},
        "cancel_order": {},
    },
    "FutureMarket": {
        "get_groups": {},
        "get_last_price": {},
        "get_ticker": {},
        "get_trade_history": {},
        "get_depth": {},
        "get_swap_history": {},
    },
    "MarginTrade": {
        "get_positions": {},
        "position_history": {},
        "get_active_positions": {},
        "create_position": {},
        "update_position": {},
        "cancel_position": {},
    }
}
