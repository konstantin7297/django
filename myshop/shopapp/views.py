from math import ceil

from django.db.models import Q
from django.http import HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoriesView(ListAPIView):
    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializer


class CatalogView(ListAPIView):
    queryset = Product.objects.prefetch_related("tags", "orders", "images").select_related("category")

    def get(self, request: Request, *args, **kwargs):
        """  Данные фильтрации для шаблона
        {
            # 'filter[name]': '',
            # 'filter[minPrice]': '0',
            # 'filter[maxPrice]': '50000',
            # 'filter[freeDelivery]': 'false',
            # 'filter[available]': 'true',
            # 'currentPage': '1',
            # 'sort': 'price',
            # 'sortType': 'inc',
            # 'limit': '20'
        }
        """
        data = request.query_params.dict()
        start_row = max((int(data.get("currentPage", 1)) - 1) * int(data.get("limit", 20)), 1)
        end_row = int(data.get("currentPage", 1)) * int(data.get("limit", 20)) + 1

        result = self.get_queryset().filter(
            Q(name__icontains=data.get('filter[name]')) if data.get('filter[name]') else Q(),
            price__gte=float(data.get('filter[minPrice]')),
            price__lte=float(data.get('filter[maxPrice]')),
            freeDelivery=bool(data.get('filter[freeDelivery]').capitalize()),
            count__gt=0 if bool(data.get('filter[available]').capitalize()) else Q(),
        ).order_by('price' if data.get('sortType') == 'inc' else '-price')[start_row:end_row]

        return Response({
            "items": ProductSerializer(result, many=True).data,
            "currentPage": data.get("currentPage", 1),
            "lastPage": ceil(len(result) / 20)
        })


class ProductsPopularView(ListAPIView):
    pass


class ProductsLimitedView(ListAPIView):
    pass


class ProductReviewView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class ProductByIdView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class OrdersView(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class OrdersByIdView(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class SalesView(ListAPIView):
    pass


class BannersView(ListAPIView):
    pass


class BasketView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("")

    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class TagsView(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response("")
