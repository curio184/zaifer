import time
from datetime import datetime
from decimal import Decimal


class NumericConverter:
    """
    数値と文字列を相互変換するクラス
    """

    @staticmethod
    def decimal_to_str(value: Decimal) -> str:
        if value == value.to_integral_value():
            return str(value.quantize(Decimal(1)))
        else:
            return str(value.normalize())


class TimeConverter:
    """
    datetime/unixtimeを相互変換するクラス
    """

    @staticmethod
    def datetime_to_unixtime(from_datetime: datetime) -> float:
        """
        datetimeからunixtimeに変換する
        """
        return time.mktime(from_datetime.timetuple())

    @staticmethod
    def unixtime_to_datetime(from_unixtime: float) -> datetime:
        """
        unixtimeからdatettimeに変換する
        """
        return datetime.fromtimestamp(from_unixtime)

    @staticmethod
    def datetime_to_str(from_datetime: datetime) -> float:
        """
        datetimeからstrに変換する
        """
        return "{0:%Y-%m-%d %H:%M:%S}".format(from_datetime)

    @staticmethod
    def unixtime_to_str(from_unixtime: float) -> datetime:
        """
        unixtimeからstrに変換する
        """
        return "{0:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(from_unixtime))
