import logging
import re
import jinja2
from markupsafe import escape
from spaceone.core import utils
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)

JINJA_ENV = jinja2.Environment(loader=jinja2.BaseLoader(), autoescape=True)


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, data):
        """ Data Structure
        {
            'event_key': 'str',
            'event_type': 'ALERT' | 'RECOVERY',
            'title': 'str',
            'description': 'str',
            'severity': 'CRITICAL' | 'ERROR' | 'WARNING' | 'INFO' | 'NOT_AVAILABLE' | NONE(default),
            'rule': 'str',
            'image_url': 'str',
            'resource': {
                'resource_id': 'str',
                'resource_type': 'str',
                'name': 'str'
            },
            'additional_info': 'dict',
            'occurred_at': 'datetime'
        }
        """
        try:
            event_model = EventModel(data, strict=False)
            event_model.validate()
            return [event_model.to_native()]
        except Exception as e:
            _LOGGER.error(f"Event parsing error: {e}", exc_info=True)
            raise ERROR_EVENT_PARSE()

    def change_data_by_options(self, options: dict, data: dict) -> dict:
        if load_json := options.get("load_json"):
            data = self._load_json_data(data, load_json)

        if convert_data := options.get("convert_data"):
            data = self._convert_data(data, convert_data)
        return data

    @staticmethod
    def _sanitize_input(value: str) -> str:
        return re.sub(r"<.*?>", "", value)

    @staticmethod
    def _convert_data(data: dict, option: dict) -> dict:
        converted_data = {}

        for key in option.keys():
            if key in ["resource", "additional_info"]:
                if key not in converted_data:
                    converted_data[key] = {}

                for sub_key in option[key].keys():
                    template = option[key].get(sub_key)

                    template = escape(template)
                    jinja_template = JINJA_ENV.from_string(template)

                    template_applied_value = jinja_template.render(**{
                        k: escape(v) if isinstance(v, str) else v
                        for k, v in data.items()
                    })

                    converted_data[key][sub_key] = template_applied_value

            else:
                template = option.get(key)
                template = escape(template)
                jinja_template = JINJA_ENV.from_string(template)

                template_applied_value = jinja_template.render(**{
                    k: escape(v) if isinstance(v, str) else v
                    for k, v in data.items()
                })

                converted_data[key] = template_applied_value

        return converted_data

    @staticmethod
    def _load_json_data(data: dict, option: str) -> dict:
        for key in option:
            json_str = utils.get_dict_value(data, key)
            if json_str:
                try:
                    json_data = utils.load_json(json_str)
                    utils.change_dict_value(data, key, json_data)
                except Exception as e:
                    _LOGGER.error(f"Failed to load json data: {e}", exc_info=True)
                    raise ERROR_EVENT_PARSE()

        return data