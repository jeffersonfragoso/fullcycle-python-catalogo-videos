from typing import Callable
from core.category.application.dto import CategoryOutput
from core.category.infra.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from core.category.application.use_cases import CreateCategoryUseCase, DeleteCategoryUseCase, GetCategoryUseCase, ListCategoriesUseCase, UpdateCategoryUseCase
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(**serializer.validated_data)
        output = self.create_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body, status=HTTP_201_CREATED)

    def get(self, request: Request, id: str = None): # pylint: disable=redefined-builtin, invalid-name
      if id:
        return self.get_object(id)
      input_param = ListCategoriesUseCase.Input(
          **request.query_params.dict())
      output = self.list_use_case().execute(input_param)
      return Response(asdict(output))

    def get_object(self, id: str):  # pylint: disable=redefined-builtin, invalid-name
      input_param = GetCategoryUseCase.Input(id)
      output = self.get_use_case().execute(input_param)
      body = CategoryResource.category_to_response(output)
      return Response(body)

    def put(self, request: Request, id: str):
      serializer = CategorySerializer(data=request.data)
      serializer.is_valid(raise_exception=True)# pylint: disable=redefined-builtin, invalid-name

      input_param = UpdateCategoryUseCase.Input(**{'id':id, **serializer.validated_data})
      output = self.update_use_case().execute(input_param)
      body = CategoryResource.category_to_response(output)
      return Response(body)

    def delete(self, _request: Request,  id: str):  # pylint: disable=redefined-builtin, invalid-name
      input_param = DeleteCategoryUseCase.Input(id=id)
      self.delete_use_case().execute(input_param)
      return Response(status=HTTP_204_NO_CONTENT)

    @staticmethod
    def category_to_response(output: CategoryOutput):
      serializer = CategorySerializer(instance=output)
      return serializer.data
