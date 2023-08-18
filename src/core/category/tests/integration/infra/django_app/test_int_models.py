# pylint: disable=no-member
from datetime import datetime
from django.utils import timezone
import pytest
import unittest

from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):

    def test_mapping(self):
        table_name = CategoryModel._meta.db_table
        self.assertEqual(table_name, 'categories')

        fields_name = tuple(field.name for field in CategoryModel._meta.fields)
        self.assertEqual(fields_name, ('id', 'name', 'description', 'is_active', 'created_at'))

    def test_create(self):

        arrange = {
            "id": "11ed3535-7af7-4d9d-80a7-245a2121954c",
            "name": "Movie",
            "description": None,
            "is_active": True,
            "created_at": timezone.now()
        }

        category = CategoryModel.objects.create(**arrange)
        self.assertEqual(category.id, arrange['id'])
        self.assertEqual(category.name, arrange['name'])
        self.assertEqual(category.description, arrange['description'])
        self.assertEqual(category.is_active, arrange['is_active'])
