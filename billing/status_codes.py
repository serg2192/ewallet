
STATUS_CODES = {
    'SUCCESS': 0,
    'UNKNOWN_ERROR': 1,
    'INVALID_INPUT_PARAMS': 100,
    'NOT_FOUND': 101,
    'NOT_ENOUGH_MONEY': 102
}

SUCCESS = STATUS_CODES['SUCCESS']
UNKNOWN_ERROR = STATUS_CODES['UNKNOWN_ERROR']
INVALID_INPUT_PARAMS = STATUS_CODES['INVALID_INPUT_PARAMS']


MESSAGES = {
    'generic': {
        0: 'Успех',
        1: 'Неизвестная ошибка',
        100: 'Переданы неверные входные параметры',
        101: 'Не найдено',
    },
    # here you can write the specific message for route
    # '/path_to_nowhere': {
    #     100: 'some specific message',
    # }
}


def get_message(request, code):
    key = request.path
    if key not in MESSAGES:
        message = MESSAGES.get('generic', {}).get(code, '')
    else:
        # specific message for url
        message = MESSAGES[key].get(code, '')
    return message
