from billing.status_codes import INVALID_INPUT_PARAMS


class CodeError(Exception):
    _code = None
    _msg = None

    def __init__(self, *, code=None, msg=None, details=None, **kwargs):
        self.code = code or self._code
        self.msg = msg or self._msg
        self.details = details
        self.extra_data = kwargs


class InvalidInputParamsError(CodeError):
    _code = INVALID_INPUT_PARAMS
