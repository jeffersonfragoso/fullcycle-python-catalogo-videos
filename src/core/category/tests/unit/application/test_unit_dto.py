# pylint: disable=R0801

from datetime import datetime
from typing import Optional
import unittest

from core.category.application.dto import CategoryOutPutMapper, CategoryOutput
from core.category.domain.entities import Category


class TestCategoryOutputUnit(unittest.TestCase):

    def test_fields(self):

        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime
        })


class CategoryOutputChild(CategoryOutput):
    pass


class TestCategoryOutputMapperUnit(unittest.TestCase):

    def test_to_output_from_child(self):
        mapper = CategoryOutPutMapper\
            .from_child(CategoryOutputChild)
        self.assertIsInstance(mapper, CategoryOutPutMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOutputChild
            )
        )

    def test_to_output_without_child(self):
        mapper = CategoryOutPutMapper.without_child()
        self.assertIsInstance(mapper, CategoryOutPutMapper)
        self.assertTrue(
            issubclass(
                mapper.output_child,
                CategoryOutput
            )
        )

    def test_to_output(self):
        created_at = datetime.now()
        category = Category(
            name="test",
            description="some description",
            is_active=True,
            created_at=created_at
        )
        output = CategoryOutPutMapper.without_child().to_output(category)
        self.assertEqual(output, CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        ))

        output = CategoryOutPutMapper.from_child(
            CategoryOutputChild).to_output(category)
        self.assertEqual(output, CategoryOutputChild(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        ))
