from typing import List
from django.core import exceptions as django_exceptions
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityID
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.models import CategoryModel


class CategoryDjangoRepository(CategoryRepository):

    def insert(self, entity: Category) -> None:
        CategoryModel.objects.create(**entity.to_dict())

    def find_by_id(self, entity_id: str | UniqueEntityID) -> Category:
      model = self._get(str(entity_id))
      return Category(
        unique_entity_id=UniqueEntityID(str(entity_id)),
        name=model.name,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at
      )

    def find_all(self) -> List[Category]:
        raise NotImplementedError()

    def update(self, entity: Category) -> None:
        raise NotImplementedError()

    def delete(self, entity_id: str | UniqueEntityID) -> None:
        raise NotImplementedError()

    def search(self, input_params: CategoryRepository.SearchParams) -> CategoryRepository.SearchResult:
      raise NotImplementedError()

    def _get(self, entity_id: str) -> CategoryModel:
      try:
          return CategoryModel.objects.get(pk=entity_id)
      except (CategoryModel.DoesNotExist, django_exceptions.ValidationError) as exception:
          raise NotFoundException(f"Entity not found using ID '{entity_id}'") from exception
