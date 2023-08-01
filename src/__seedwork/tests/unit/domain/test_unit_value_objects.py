import unittest
import uuid
from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
from unittest.mock import patch

from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityID, ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str

@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str

class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, 'value')

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(vo2.prop1, 'value1')
        self.assertEqual(vo2.prop2, 'value2')

    def test_convert_to_string(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, str(vo1))

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
          value_object = StubOneProp(prop='value')
          value_object.prop = 'fake'

class TestUniqueEntityIdUnit(unittest.TestCase):

  def test_if_is_a_dataclass(self):
    self.assertTrue(is_dataclass(UniqueEntityID))

  def test_throw_exception_when_uuid_is_invalid(self):
    with patch.object(
      UniqueEntityID,
      '_UniqueEntityID__validate',
      autospec=True,
      side_effect=UniqueEntityID._UniqueEntityID__validate
    ) as mock_validate:
      with self.assertRaises(InvalidUuidException) as assert_error:
        UniqueEntityID('fake id')
      mock_validate.assert_called_once()
      self.assertEqual(assert_error.exception.args[0], 'Id must be a valid UUID')

  def test_accept_uuid_passed_in_constructor(self):
    with patch.object(
      UniqueEntityID,
      '_UniqueEntityID__validate',
      autospec=True,
      side_effect=UniqueEntityID._UniqueEntityID__validate
    ) as mock_validate:
      value_object = UniqueEntityID('c71404e4-1a1f-4587-9ff1-5e6b90589a81')
      mock_validate.assert_called_once()
      self.assertEqual(value_object.id, 'c71404e4-1a1f-4587-9ff1-5e6b90589a81')

    uuid_value = uuid.uuid4()
    value_object = UniqueEntityID(uuid_value)
    self.assertEqual(value_object.id, str(uuid_value))

  def test_generate_id_when_no_passed_id_in_constructor(self):
    with patch.object(
      UniqueEntityID,
      '_UniqueEntityID__validate',
      autospec=True,
      side_effect=UniqueEntityID._UniqueEntityID__validate
    ) as mock_validate:
      value_object = UniqueEntityID()
      mock_validate.assert_called_once()

  def test_is_immutable(self):
    with self.assertRaises(FrozenInstanceError):
        value_object = UniqueEntityID()
        value_object.id = "fake id"
