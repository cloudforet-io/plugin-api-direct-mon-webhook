import logging
import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json
import datetime

_LOGGER = logging.getLogger(__name__)
TEST_JSON = os.environ.get('test_json', None)


class TestEvent(TestCase):

    def test_parse(self):
        params = {
            "options": {

            },
            "data": {
                "event_key": "event-x1234vlkajdflk",
                "event_type": "ALERT",
                "title": "This is test event",
                "description": "EAEAEAEAEAEAEA",
                "severity": "ERROR",
                "rule": "AAAAAAAA",
                "image_url": "https://aaaaaa/img/sdfsdf",
                "resource": {
                    "resource_id": "resource-xzasdfasdf",
                    "resource_type": "server",
                    "name": "asdfasldkfjaslkdfj"
                },
                "additional_info": {
                    "asdlkafjsdlkf": "asdfasdf"
                },
                "occurred_at": datetime.datetime.utcnow().isoformat()
            }
        }

        test_cases = [params]

        for idx, test_case in enumerate(test_cases):
            print(f'###### {idx} ########')
            parsed_data = self.monitoring.Event.parse({'options': {}, 'data': test_case.get('data')})
            print_json(parsed_data)
            print()


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
