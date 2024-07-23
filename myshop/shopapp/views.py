from decimal import Decimal
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
    queryset = Product.objects.prefetch_related("tags", "images").select_related("category")

    def get(self, request: Request, *args, **kwargs):
        data = request.query_params.dict()
        page = int(data.get("currentPage", 1))
        limit = int(data.get("limit", 20))
        start_row = max((page - 1) * limit, 1)
        end_row = page * limit + 1

        result = self.get_queryset().filter(
            Q(name__icontains=data.get('filter[name]', "")) if data.get('filter[name]', "") else Q(),
            price__gte=Decimal(data.get('filter[minPrice]', 0)),
            price__lte=Decimal(data.get('filter[maxPrice]', 9999999999)),
            freeDelivery=bool(data.get('filter[freeDelivery]', "false").capitalize()),
            count__gt=0 if bool(data.get('filter[available]', "true").capitalize()) else Q(),
        ).order_by('price' if data.get('sortType', "dec") == 'inc' else '-price')[start_row:end_row]

        return Response({
            "items": ProductSerializer(result, many=True).data,
            "currentPage": page,
            "lastPage": ceil(len(result) / limit)
        })


class ProductsPopularView(ListAPIView):
    """В каталог топ-товаров попадают восемь первых товаров по параметру «индекс
    сортировки». Если же индекс сортировки совпадает, то товары сортируются
    по количеству покупок."""
    queryset = Product.objects.prefetch_related("tags", "images").select_related("category")[:8]
    serializer_class = ProductSerializer


class ProductsLimitedView(ListAPIView):
    """В блок «Ограниченный тираж» попадают до 16 товаров с галочкой
    «ограниченный тираж». Отображаются эти товары в виде слайдера."""
    queryset = Product.objects.prefetch_related("tags", "images").select_related("category")[:16]
    serializer_class = ProductSerializer


class ProductReviewView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class ProductByIdView(APIView):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get("id"))
        return Response(ProductSerializer(product).data)


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
