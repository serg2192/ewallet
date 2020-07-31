from billing.errors import CodeError
from billing.status_codes import STATUS_CODES


class DBBaseError(CodeError):
    ...


class UserNotFoundError(DBBaseError):
    _code = STATUS_CODES['NOT_FOUND']
    _msg = 'Пользователь не найден'


class NotEnoughMoneyError(DBBaseError):
    _code = STATUS_CODES['NOT_ENOUGH_MONEY']
    _msg = "Не хватает денюшек"
