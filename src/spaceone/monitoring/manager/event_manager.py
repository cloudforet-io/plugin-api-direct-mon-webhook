import logging

from spaceone.core.utils import *
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, data):
        """ data sample
            "data": {
                "event_key": "",
                "event_type": "ALERT" | "RECOVERY",
                "title": "",
                "description": "",
                "severity": "CRITICAL" | "ERROR" | "WARNING" | "INFO" | "NOT_AVAILABLE" | NONE(default),
                "rule": "",
                "image_url": "",
                "resource": {
                    "resource_id",
                    "resource_type",
                    "name"
                },
                "additional_info": {
                },
                "occurred_at": ""
            }
        """

        try:
            data.update({
                "occurred_at": iso8601_to_datetime(data.get('occurred_at'))
            })

            event_model = EventModel(data, strict=False)
            event_model.validate()
            return [event_model.to_native()]

        except Exception as e:
            raise ERROR_EVENT_PARSE()
