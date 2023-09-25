
# pylint: disable=unexpected-keyword-arg,no-member

import unittest
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityID
import pytest
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from core.category.infra.django_app.models import CategoryModel
from core.category.domain.entities import Category


@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self):
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(
            name='Movie',
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie')
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name='Movie 2',
            description='Movie description',
            is_active=False
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie 2')
        self.assertEqual(model.description, 'Movie description')
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('af46842e-027d-4c91-b259-3a3642144ba4')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'")

        unique_entity_id = UniqueEntityID(
            'af46842e-027d-4c91-b259-3a3642144ba4')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'"
        )

    def test_find_by_id(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)

        category_found = self.repo.find_by_id(category.id)
        self.assertEqual(category_found, category)

        category_found = self.repo.find_by_id(category.unique_entity_id)
        self.assertEqual(category_found, category)
