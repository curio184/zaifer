

class InvalidAPIKeyException(Exception):
    '''
    API Keyが不正です。
    '''
    pass


class InvalidAPISecretException(Exception):
    '''
    API Secretが不正です。
    '''
    pass


class OrderNotFoundException(Exception):
    '''
    注文が存在しません。
    '''
    pass


class NonceNotIcreasedException(Exception):
    '''
    ナンスが増加されていません。
    '''
    pass


class NonceOutOfRangeException(Exception):
    '''
    ナンスが範囲外です。
    '''
    pass


class TradeTemporarilyUnavailableException(Exception):
    '''
    お取引が一時的に利用できません。
    '''
    pass


class InvalidAmountException(Exception):
    '''
    数量が不正です。
    '''
    pass
