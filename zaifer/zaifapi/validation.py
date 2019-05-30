from inspect import signature

from cerberus import Validator
from zaifer.zaifapi.validation_schema import zaifapi_schema


def zaifapi_schema_validator(func):
    """
    ZaifApiの呼び出しパラメータが妥当であるか確認します。
    """

    def wrapper(*args, **kwargs):

        # デコレーターの呼び出し元の情報を取得する
        class_name = args[0].__class__.__name__     # クラス名
        func_name = func.__name__                   # ファンクション名

        # 検証スキーマが定義されていることを確認する
        do_validate = False
        if class_name in zaifapi_schema:
            if func_name in zaifapi_schema[class_name]:
                do_validate = True

        # 検証スキーマが定義されている場合
        if do_validate:

            # 引数をdict形式にバインドする
            sig = signature(func)
            bound_args = sig.bind(*args)
            bound_args = dict(bound_args.arguments)
            del bound_args["self"]

            # 引数の値を検証する
            v = Validator(zaifapi_schema[class_name][func_name])
            if not v.validate(bound_args):
                raise Exception(v.errors)
        else:
            print("validation shcema isn't defined.")

        return func(*args, **kwargs)

    return wrapper
