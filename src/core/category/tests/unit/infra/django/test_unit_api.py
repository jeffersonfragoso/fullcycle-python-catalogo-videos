from dataclasses import asdict
from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from core.category.infra.django_app.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):

    def __init_all_none(self):
      return {
          'get_use_case': None,
          'create_use_case': None,
          'list_use_case': None,
          'update_use_case': None,
          'delete_use_case': None
      }

    def test_post_method(self):
        send_data = {'name': 'Movie'}
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)
        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='c71404e4-1a1f-4587-9ff1-5e6b90589a81',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'create_use_case': lambda: mock_create_use_case
            }
        )

        _request = APIRequestFactory().post('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.post(request)
        mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
            name='Movie'
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            asdict(mock_create_use_case.execute.return_value)
        )


    def test_get_method(self):
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)
        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[CategoryOutput(
                id='c71404e4-1a1f-4587-9ff1-5e6b90589a81',
                name='Movie',
                description=None,
                is_active=True,
                created_at=datetime.now()
            )],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )
        resource = CategoryResource(
          **{
            **self.__init_all_none(),
            'list_use_case': lambda: mock_list_use_case
          }
        )

        _request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test')
        request = Request(_request)
        response = resource.get(request)
        mock_list_use_case.execute.assert_called_with(ListCategoriesUseCase.Input(
            page="1",
            per_page="1",
            sort="name",
            sort_dir="asc",
            filter="test"
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            asdict(mock_list_use_case.execute.return_value)
        )

    def test_if_get_invoke_get_object(self):
      resource = CategoryResource(**self.__init_all_none())
      resource.get_object = mock.Mock()
      resource.get(None, 'c71404e4-1a1f-4587-9ff1-5e6b90589a81')
      resource.get_object.assert_called_once_with(
          'c71404e4-1a1f-4587-9ff1-5e6b90589a81')

    def test_get_object_method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='c71404e4-1a1f-4587-9ff1-5e6b90589a81',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'get_use_case': lambda: mock_get_use_case
            }
        )

        response = resource.get_object('c71404e4-1a1f-4587-9ff1-5e6b90589a81')
        mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
            id='c71404e4-1a1f-4587-9ff1-5e6b90589a81'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            asdict(mock_get_use_case.execute.return_value)
        )

    def test_put_method(self):
        send_data = {
          'id': 'c71404e4-1a1f-4587-9ff1-5e6b90589a81',
          'name': 'Movie'
        }
        mock_update_use_case = mock.Mock(UpdateCategoryUseCase)
        mock_update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id=send_data['id'],
            name=send_data['name'],
            description=None,
            is_active=True,
            created_at=datetime.now()
        )
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'update_use_case': lambda: mock_update_use_case
            }
        )
        _request = APIRequestFactory().put('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.put(
            request, send_data["id"]
        )
        mock_update_use_case.execute.assert_called_with(UpdateCategoryUseCase.Input(
            id=send_data["id"],
            name=send_data["name"]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            asdict(mock_update_use_case.execute.return_value)
        )

    def test_delete_method(self):
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)
        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'delete_use_case': lambda: mock_delete_use_case
            }
        )

        _request = APIRequestFactory().delete('/')
        request = Request(_request)
        response = resource.delete(
            request, id='c71404e4-1a1f-4587-9ff1-5e6b90589a81'
        )

        mock_delete_use_case.execute.assert_called_with(DeleteCategoryUseCase.Input(
            id='c71404e4-1a1f-4587-9ff1-5e6b90589a81'
        ))
        self.assertEqual(response.status_code, 204)
