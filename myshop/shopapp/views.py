import os
from math import ceil
from decimal import Decimal

from django.db import transaction
from django.db.models import Q, Avg, F, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Tag, Product, ProductImage, Review, Basket, Order, Payment
from .serializers import (
    CategorySerializer,
    TagSerializer,
    FullProductSerializer,
    ReviewSerializer,
    ShortProductSerializer,
    OrderSerializer,
)


def get_session(request: Request) -> int:
    """ function for getting user session """
    session = request.session.get("user", None)
    if not session:
        session = len(Basket.objects.order_by().values("user").distinct()) + 1
        request.session["user"] = session
    return session


class CategoriesView(ListAPIView):
    """ View for listing all categories """
    queryset = Category.objects.prefetch_related("subcategories")
    serializer_class = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


class CatalogView(ListAPIView):
    """ View for listing filtered products """
    queryset = Product.objects.prefetch_related(
        "tags", "images"
    ).select_related("category").filter(sale=False)
    serializer_class = ShortProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
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
            "items": self.serializer_class(result, many=True).data,
            "currentPage": page,
            "lastPage": ceil(len(result) / limit)
        })


class ProductsPopularView(ListAPIView):
    """ View for listing all popular products """
    queryset = (
        Product.objects
        .prefetch_related("tags", "images", "baskets")
        .select_related("category")
        .filter(sale=False)
        .annotate(selling=Sum("baskets__count", default=0))
        .order_by("price", "selling")[:8]
    )
    serializer_class = ShortProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


class ProductsLimitedView(ListAPIView):
    """ View for listing products limited """
    queryset = Product.objects.prefetch_related(
        "tags", "images"
    ).select_related("category").filter(limited=True, sale=False)[:16]
    serializer_class = ShortProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


class SalesView(ListAPIView):  # TODO
    """ View for listing all sales orders """
    pass


class BannersView(ListAPIView):  # TODO
    """ View for listing all banners """
    pass


class BasketView(APIView):
    """ View for basket operations """
    @staticmethod
    def get(request: Request, *args, **kwargs) -> Response:
        basket_products: list = list()

        for basket in Basket.objects.select_related(
                "product"
        ).filter(user=get_session(request)):
            product = basket.product
            product.count = basket.count
            basket_products.append(product)

        return Response(ShortProductSerializer(basket_products, many=True).data)

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        session = get_session(request)

        count = request.data.get("count", 1)
        product = Product.objects.filter(
            pk=request.data.get("id"),
            count__gte=count,
            sale=False
        )

        if product:
            product = product[0]

            product.count = F("count") - count
            basket = Basket.objects.filter(user=session, product=product)

            if basket:
                basket = basket[0]
                basket.count = F("count") + count
                basket.save(update_fields=["count"])

            else:
                basket = Basket.objects.create(
                    user=session, count=count, product=product
                )
                basket.save()

            product.save(update_fields=["count"])
            return self.get(request, *args, **kwargs)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request: Request, *args, **kwargs) -> Response:
        session = get_session(request)

        count = request.data.get("count", 1)
        product = Product.objects.get(pk=request.data.get("id"))

        baskets = Basket.objects.filter(
            user=session,
            product=product,
        )

        if baskets:
            baskets = baskets[0]
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if baskets.count > count:
            baskets.count = F("count") - count
            product.count = F("count") + count
            baskets.save(update_fields=["count"])
            product.save(update_fields=["count"])

        else:
            product.count = F("count") + baskets.count
            baskets.delete()
            product.save(update_fields=["count"])

        return self.get(request, *args, **kwargs)


class OrdersView(APIView):
    """ View for main operation with orders """
    @staticmethod
    def get(request: Request, *args, **kwargs) -> Response:
        orders = Order.objects.prefetch_related("products").all()
        return Response(OrderSerializer(orders, many=True).data)

    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        order = Order.objects.create()
        order.save()

        for product in request.data:
            product_obj = Product.objects.get(pk=product.get("id"))

            product_obj.count = product.get("count")
            product_obj.sale = True
            product_obj.id = None
            sale_product = Product.objects.bulk_create([product_obj])

            if sale_product:
                image_obj = ProductImage.objects.filter(
                    product__id=product.get("id")
                ).first()

                ProductImage.objects.create(
                    product=sale_product[0], image=image_obj.image
                )

                order.products.add(sale_product[0])
                order.totalCost = F("totalCost") + (
                        product.get("price") * product.get("count")
                )

        order.save(update_fields=["totalCost"])
        return Response({"orderId": order.id})


class OrdersByIdView(APIView):
    """ View for getting and updating orders by id """
    @staticmethod
    def get(request: Request, *args, **kwargs) -> Response:
        order = Order.objects.prefetch_related("products").get(pk=kwargs.get("id"))
        return Response(OrderSerializer(order).data)

    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        order = Order.objects.get(pk=kwargs.get("id"))
        data = request.data

        if data.get("deliveryType") == "ordinary":
            if float(data.get("totalCost")) < float(os.getenv("delivery_check", 2000)):
                data["totalCost"] = float(data["totalCost"]) + int(
                    os.getenv("delivery_ordinary", 200)
                )

        elif data.get("deliveryType") == "express":
            data["totalCost"] = float(data["totalCost"]) + int(
                os.getenv("delivery_express", 500)
            )

        serializer = OrderSerializer(data=data, instance=order)

        if serializer.is_valid():
            serializer.update(instance=order, validated_data=serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentView(APIView, LoginRequiredMixin):
    """ View for payments """
    @staticmethod
    @transaction.atomic
    def post(request: Request, *args, **kwargs) -> Response:
        order = Order.objects.get(pk=kwargs.get("id"))
        Payment.objects.create(
            order=order,
            number=int(request.data.get("number")),
            name=request.data.get("name"),
            month=int(request.data.get("month")),
            year=int(request.data.get("year")),
            code=int(request.data.get("code")),
        )
        return Response(status=status.HTTP_200_OK)


class TagsView(ListAPIView):
    """ View for listing all tags by category """
    queryset = Tag.objects
    serializer_class = TagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


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
    def post(request: Request, *args, **kwargs) -> Response:
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
