import logging
from spaceone.core.service import *
from spaceone.core.utils import *
from spaceone.monitoring.error.event import *
from spaceone.monitoring.manager.event_manager import EventManager

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA = 'aws_access_key'

@authentication_handler
@authorization_handler
@event_handler
class EventService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_mgr: EventManager = self.locator.get_manager('EventManager')

    @transaction
    @check_required(['options', 'data'])
    def parse(self, params):
        """
        Args:
            params (dict): {
                'options': 'dict',
                'raw_data': 'dict'
            }

        Returns:
            plugin_metric_data_response (dict)
        """

        options = params.get('options', {})
        data = params.get('data', {})

        self.validate_additional_info_data(data)

        data.update({
            "occurred_at": iso8601_to_datetime(data.get('occurred_at'))
        })

        parsed_event = self.event_mgr.parse(options, data)
        _LOGGER.debug(f'[EventService: parse] {parsed_event}')
        return parsed_event

    @staticmethod
    def validate_additional_info_data(data):
        if additional_info := data.get('additional_info', {}):
            for _k, _v in additional_info.items():
                try:
                    additional_info[str(_k)] = str(_v)
                except:
                    del additional_info[_k]
