import logging

from spaceone.core.service import *
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class WebhookService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @check_required(['options'])
    def init(self, params: dict) -> dict:
        """ Init webhook
        Args:
            params (dict): {
                'options': 'dict',      # required
            }

        Returns:
            webhook_data (dict)
        """

        self._check_options(params['options'])
        return {'metadata': {}}

    @transaction
    @check_required(['options'])
    def verify(self, params: dict) -> None:
        """ Init webhook
        Args:
            params (dict): {
                'options': 'dict',      # required
            }

        Returns:
            None
        """
        pass

    @staticmethod
    def _check_options(options):
        for key, value in options.items():
            if key == 'load_json':
                if not isinstance(value, list):
                    raise ERROR_INVALID_PARAMETER_TYPE(key='options.load_json', type='list')
            elif key == 'convert_data':
                if not isinstance(value, dict):
                    raise ERROR_INVALID_PARAMETER_TYPE(key='options.convert_data', type='dict')
            elif key == 'confirm_url':
                if not isinstance(value, str):
                    raise ERROR_INVALID_PARAMETER_TYPE(key='options.confirm_url', type='str')
            else:
                raise ERROR_NOT_SUPPORTED_OPTION(key=key)
