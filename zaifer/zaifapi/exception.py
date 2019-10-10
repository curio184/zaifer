

class InvalidAPIKeyException(Exception):
    '''
    API Keyが不正です。
    '''


class InvalidAPISecretException(Exception):
    '''
    API Secretが不正です。
    '''


class OrderNotFoundException(Exception):
    '''
    注文が存在しません。
    '''


class NonceNotIcreasedException(Exception):
    '''
    ナンスが増加されていません。
    '''


class NonceOutOfRangeException(Exception):
    '''
    ナンスが範囲外です。
    '''


class TradeTemporarilyUnavailableException(Exception):
    '''
    お取引が一時的に利用できません。
    '''


class InvalidAmountException(Exception):
    '''
    数量が不正です。
    '''


class TimeoutException(Exception):
    '''
    リクエストがタイムアウトしました。
    '''
