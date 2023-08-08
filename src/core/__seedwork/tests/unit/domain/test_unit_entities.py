from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import UniqueEntityID


@dataclass(kw_only=True, frozen=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self):
        entity = StubEntity(prop1='value1', prop2='value2')
        self.assertEqual(entity.prop1, 'value1')
        self.assertEqual(entity.prop2, 'value2')
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityID)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityID(
                'c71404e4-1a1f-4587-9ff1-5e6b90589a81'),
            prop1='value',
            prop2='value2'
        )
        self.assertEqual(entity.id, 'c71404e4-1a1f-4587-9ff1-5e6b90589a81')

    def test_to_dict_method(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityID(
                'c71404e4-1a1f-4587-9ff1-5e6b90589a81'),
            prop1='value1',
            prop2='value2'
        )
        self.assertDictEqual(entity.to_dict(), {
            'id': 'c71404e4-1a1f-4587-9ff1-5e6b90589a81',
            'prop1': 'value1',
            'prop2': 'value2'
        })

    def test_set_method(self):
        entity = StubEntity(prop1='value1', prop2='value2')
        entity._set('prop1', 'changed')  # pylint: disable=protected-access
        self.assertEqual(entity.prop1, 'changed')
