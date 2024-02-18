from spaceone.core.error import *


class ERROR_NOT_SUPPORTED_OPTION(ERROR_BASE):
    _message = 'Not supported option. (key = {key})'


class ERROR_EVENT_PARSE(ERROR_BASE):
    _message = 'Fail to parse the event.'
