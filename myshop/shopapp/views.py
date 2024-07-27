from math import ceil
from decimal import Decimal

from django.db import transaction
from django.db.models import Q, Avg
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Tag, Product, Review, Order, Basket
from .serializers import (
    CategorySerializer,
    TagSerializer,
    FullProductSerializer,
    ReviewSerializer,
    ShortProductSerializer,
    OrderSerializer,
)


class CategoriesView(ListAPIView):
    """ View for listing all categories """
    queryset = Category.objects.prefetch_related("subcategories")
    serializer_class = CategorySerializer


class CatalogView(ListAPIView):
    """ View for listing filtered products """
    queryset = Product.objects.prefetch_related(
        "tags", "images"
    ).select_related("category")

    def get(self, request: Request, *args, **kwargs):
        data = request.query_params.dict()
        page = int(data.get("currentPage", 1))
        limit = int(data.get("limit", 20))

        start_row = max((page - 1) * limit, 1)
        end_row = page * limit + 1

        name = data.get('filter[name]')
        price_min = Decimal(data.get('filter[minPrice]', 0))
        price_max = Decimal(data.get('filter[maxPrice]', 9999999999))
        free_delivery = bool(data.get('filter[freeDelivery]', "false").capitalize())
        available = bool(data.get('filter[available]', "true").capitalize())
        sort = data.get('sortType', "dec")

        result = self.get_queryset().filter(
            Q(name__icontains=name) if name else Q(),
            price__gte=price_min,
            price__lte=price_max,
            freeDelivery=free_delivery,
            count__gt=0 if available else Q(),
        ).order_by('price' if sort == 'inc' else '-price')[start_row:end_row]

        return Response({
            "items": ShortProductSerializer(result, many=True).data,
            "currentPage": page,
            "lastPage": ceil(len(result) / limit)
        })


class ProductsPopularView(ListAPIView):  # TODO
    """В каталог топ-товаров попадают восемь первых товаров по параметру «индекс
    сортировки». Если же индекс сортировки совпадает, то товары сортируются
    по количеству покупок."""
    queryset = Product.objects.prefetch_related("tags", "images").select_related("category")[:8]
    serializer_class = ShortProductSerializer


class ProductsLimitedView(ListAPIView):
    """ View for listing products limited """
    queryset = Product.objects.prefetch_related(
        "tags", "images"
    ).select_related("category").filter(limited=True)[:16]
    serializer_class = ShortProductSerializer


class SalesView(ListAPIView):  # TODO
    """ View for listing all sales orders """
    pass


class BannersView(ListAPIView):  # TODO
    """ View for listing all banners """
    pass


class BasketView(APIView):  # TODO
    """ View for basket operations """
    def get(self, request: Request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        get_user = request.session.get("user", None)

        if not get_user:
            pass

        print(get_user)
        if not get_user:
            request.session["user"] = 1
        return Response(f"{get_user}")
        # check_basket = Basket.objects.select_related("user").get()

    @transaction.atomic
    def delete(self, request: Request, *args, **kwargs):
        pass


class OrdersView(APIView):
    """ View for main operation with orders """
    @staticmethod
    def get(request, *args, **kwargs):
        orders = Order.objects.prefetch_related("products").all()
        return Response(OrderSerializer(orders, many=True).data)

    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs):
        order = Order.objects.create()
        order.save()

        for product in request.data:
            product_obj = Product.objects.get(pk=product.get("id"))
            order.products.add(product_obj)

        order.save(update_fields=["products"])
        return Response({"orderId": order.id})


class OrdersByIdView(APIView):
    """ View for getting and updating orders by id """
    @staticmethod
    def get(request, *args, **kwargs):
        order = Order.objects.prefetch_related("products").get(pk=kwargs.get("id"))
        return Response(OrderSerializer(order).data)

    @staticmethod
    @transaction.atomic
    def post(request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs.get("id"))
        data = request.data
        serializer = OrderSerializer(data=data, instance=order)

        if serializer.is_valid():
            serializer.update(order, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentView(APIView, LoginRequiredMixin):
    """ View for payments """
    def post(self, request: Request, *args, **kwargs) -> Response:
        pass  # TODO: В ТЗ инструкция.


class TagsView(ListAPIView):
    """ View for listing all tags by category """
    queryset = Tag.objects

    def get(self, request, *args, **kwargs):
        category = request.query_params.dict().get("category")
        if category:
            return Response(TagSerializer(
                self.get_queryset().filter(category__id=category), many=True
            ).data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductByIdView(APIView):
    """ View for getting a full product information by id """
    @staticmethod
    def get(request: Request, *args, **kwargs) -> Response:
        product = Product.objects.prefetch_related(
            "images", "tags", "reviews", "specifications"
        ).select_related("category").get(pk=kwargs.get("id"))

        if product:
            return Response(FullProductSerializer(product).data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductReviewView(APIView):
    """ View for posting reviews for a product """
    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get("id"))

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)

            rating = product.reviews.aggregate(Avg("rate"))
            product.rating = round(rating["rate__avg"], 1)
            product.save(update_fields=["rating"])

            return Response(ReviewSerializer(
                Review.objects.filter(product__id=kwargs.get("id")), many=True
            ).data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
