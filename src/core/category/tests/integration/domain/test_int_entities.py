# pylint: disable=R0801

import unittest

from core.__seedwork.domain.exceptions import EntityValidationException
from core.category.domain.entities import Category


class TestCategoryIntegration(unittest.TestCase):

    def test_create_with_invalid_cases_for_name_prop(self):

        invalid_data = [
            {'data': {'name': None}, 'expected': 'This field may not be null.'},
            {'data': {'name': ''}, 'expected': 'This field may not be blank.'},
            {'data': {'name': 5}, 'expected': 'Not a valid string.'},
            {'data': {'name': 'a'*256},
             'expected': 'Ensure this field has no more than 255 characters.'},
        ]

        for i in invalid_data:
            with self.assertRaises(EntityValidationException) as assert_error:
                Category(**i['data'])
                self.assertIn('name', assert_error.exception.error)
                self.assertListEqual(
                    assert_error.exception.error['name'],
                    [i['expected']],
                    f"Expected: {i['expected']}, actual: {assert_error.exception.error['name'][0]}"
                )

    def test_create_with_invalid_cases_for_description_prop(self):
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name=None, description=5)
            self.assertEqual(['Not a valid string.'],
                             assert_error.exception.error['description'])

    def test_create_with_invalid_cases_for_is_active_prop(self):
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name=None, is_active=5)
            self.assertEqual(['Must be a valid boolean.'],
                             assert_error.exception.error['is_active'])

    def test_create_with_valid_cases(self):
        try:
            Category(name='Movie')
            Category(name='Movie', description=None)
            Category(name='Movie', description="")
            Category(name='Movie', is_active=True)
            Category(name='Movie', is_active=False)
            Category(
                name='Movie',
                description='some description',
                is_active=False
            )
        except EntityValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.error}")

    def test_update_with_invalid_cases_for_name_prop(self):

        category = Category(name='Movie')

        invalid_data = [
            {
                'data': {'name': None, 'description': None},
                'expected': 'This field may not be null.'
            },
            {
                'data': {'name': '', 'description': None},
                'expected': 'This field may not be blank.'
            },
            {
                'data': {'name': 5, 'description': None},
                'expected': 'Not a valid string.'},
            {
                'data': {'name': 'a'*256, 'description': None},
                'expected': 'Ensure this field has no more than 255 characters.'
            },
        ]

        for i in invalid_data:
            with self.assertRaises(EntityValidationException) as assert_error:
                category.update(**i['data'])
                self.assertIn('name', assert_error.exception.error)
                self.assertListEqual(
                    assert_error.exception.error['name'],
                    [i['expected']],
                    f"Expected: {i['expected']}, actual: {assert_error.exception.error['name'][0]}"
                )

    def test_update_with_invalid_cases_for_description_prop(self):
        category = Category(name='Movie')
        with self.assertRaises(EntityValidationException) as assert_error:
            category.update(name='Movie', description=5)
        self.assertEqual(['Not a valid string.'],
                         assert_error.exception.error['description'])

    def test_update_with_valid_cases(self):
        category = Category(name='Movie')

        try:
            category.update('Movie', None)
            category.update('Movie', 'some description')
            category.update('Movie', '')
        except EntityValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.error}")
