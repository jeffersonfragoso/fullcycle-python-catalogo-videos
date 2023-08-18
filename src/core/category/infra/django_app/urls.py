from django.urls import path
from core.category.application.use_cases import CreateCategoryUseCase

from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from django_app import container
from .api import CategoryResource


def __init_category_resource():
    return {
        'create_use_case': container.use_case_category_create_category,
        'list_use_case': container.use_case_category_list_categories,
        'get_use_case': container.use_case_category_get_category,
        'update_use_case': container.use_case_category_update_category,
        'delete_use_case': container.use_case_category_delete_category
    }


urlpatterns = [
    path(
        'categories/', CategoryResource.as_view(
            **__init_category_resource()
        )),
    path(
        'categories/<uuid:id>/', CategoryResource.as_view(
            **__init_category_resource()
        ))
]
