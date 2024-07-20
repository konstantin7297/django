from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class CategoriesView(ListAPIView):
    pass


class CatalogView(ListAPIView):
    pass


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
        pass

    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class TagsView(ListAPIView):
    pass
