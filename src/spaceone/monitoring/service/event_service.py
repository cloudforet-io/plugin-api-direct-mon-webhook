import logging
import requests
from spaceone.core.service import *
from spaceone.core import utils
from spaceone.monitoring.manager.event_manager import EventManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class EventService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_mgr: EventManager = self.locator.get_manager('EventManager')

    @transaction
    @check_required(['options', 'data'])
    def parse(self, params: dict) -> list:
        """ Parse event data
        Args:
            params (dict): {
                'options': 'dict',      # required
                'data': 'dict'          # required
            }

        Returns:
            events_data (list)

        """

        options = params.get('options', {})
        data = params.get('data', {})

        if confirm_url_key := options.get('confirm_url'):
            confirm_url = utils.get_dict_value(data, confirm_url_key)
            if confirm_url:
                self._confirm_webhook(confirm_url_key, confirm_url)
                return []

        self._validate_additional_info_data(data)
        data = self.event_mgr.change_data_by_options(options, data)

        data.update({
            "occurred_at": utils.iso8601_to_datetime(data.get('occurred_at'))
        })

        parsed_event = self.event_mgr.parse(options, data)
        _LOGGER.debug(f'[EventService: parse] {parsed_event}')
        return parsed_event

    @staticmethod
    def _validate_additional_info_data(data: dict) -> None:
        if additional_info := data.get('additional_info', {}):
            for key, value in additional_info.items():
                try:
                    additional_info[str(key)] = str(value)
                except Exception as e:
                    del additional_info[key]

    @staticmethod
    def _confirm_webhook(key, confirm_url: str) -> None:
        r = requests.get(confirm_url)
        _LOGGER.debug(f'[_confirm_webhook] {key}: {confirm_url}')
        _LOGGER.debug(f'[_confirm_webhook] {r.status_code} {r.content}')
