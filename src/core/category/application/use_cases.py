# pylint: disable=invalid-name,no-member

from dataclasses import asdict, dataclass
from typing import Optional
from core.__seedwork.application.dto import (
    PaginationOutput,
    PaginationOutputMapper,
    SearchInput
)
from core.__seedwork.application.use_cases import UseCase
from core.category.application.dto import CategoryOutPutMapper, CategoryOutput

from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = Category(
            **asdict(input_param)
        )
        self.category_repo.insert(category)
        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CategoryOutPutMapper\
            .from_child(CreateCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        category = self.category_repo.find_by_id(input_param.id)
        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CategoryOutPutMapper.from_child(GetCategoryUseCase.Output).to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        search_params = self.category_repo.SearchParams(**asdict(input_param))
        result = self.category_repo.search(search_params)
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepository.SearchResult):
        items = list(
            map(CategoryOutPutMapper.without_child().to_output, result.items)
        )
        return PaginationOutputMapper\
            .from_child(ListCategoriesUseCase.Output)\
            .to_output(items, result)

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class UpdateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        entity = self.category_repo.find_by_id(input_param.id)
        entity.update(input_param.name, input_param.description)

        if input_param.is_active is True:
            entity.activate()
        if input_param.is_active is False:
            entity.deactivate()

        self.category_repo.update(entity)
        return self.__to_output(entity)

    def __to_output(self, category: Category):
        return CategoryOutPutMapper.from_child(UpdateCategoryUseCase.Output).to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str
        name: str
        description: Optional[str] = Category.get_field(
            'description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_param: 'Input') -> None:
        self.category_repo.delete(input_param.id)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str
