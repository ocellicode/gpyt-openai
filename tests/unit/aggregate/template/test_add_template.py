import unittest
from uuid import uuid4

from gpyt_openai.aggregate.template.add_template import AddTemplate
from gpyt_openai.interface.template import Template


class TestAddTemplate(unittest.TestCase):
    def test_add_one_template_created(self):
        the_uuid = uuid4()
        event = {
            "event_type": "template_created",
            "aggregate_id": the_uuid,
            "data": {"name": "value1", "body": "value2"},
        }
        state = []
        expected_state = [Template(aggregate_id=the_uuid, name="value1", body="value2")]

        new_state = AddTemplate.add_one(event, state)
        self.assertEqual(new_state, expected_state)

    def test_add_one_template_not_created(self):
        event = {
            "event_type": "some_other_event",
            "aggregate_id": uuid4(),
            "data": {"field1": "value1", "field2": "value2"},
        }
        state = []
        expected_state = []

        new_state = AddTemplate.add_one(event, state)
        self.assertEqual(new_state, expected_state)
