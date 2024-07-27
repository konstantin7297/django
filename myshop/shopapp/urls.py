from django.urls import path

from .views import (
    CategoriesView,
    CatalogView,
    ProductsPopularView,
    ProductsLimitedView,
    ProductReviewView,
    ProductByIdView,
    OrdersView,
    OrdersByIdView,
    SalesView,
    BannersView,
    BasketView,
    TagsView,
    PaymentView,
)

app_name = 'shopapp'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name="categories"),
    path('catalog', CatalogView.as_view(), name="catalog"),
    path('catalog/', CatalogView.as_view(), name="catalog"),
    path('products/popular/', ProductsPopularView.as_view(), name="products-popular"),
    path('products/limited/', ProductsLimitedView.as_view(), name="products-limited"),
    path('sales/', SalesView.as_view(), name="sales"),
    path('banners/', BannersView.as_view(), name="banners"),
    path('basket/', BasketView.as_view(), name="basket"),
    path('orders/', OrdersView.as_view(), name="orders"),
    path('orders/<int:id>/', OrdersByIdView.as_view(), name="orders-by-id"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path('tags/', TagsView.as_view(), name="tags"),
    path('product/<int:id>/', ProductByIdView.as_view(), name="product-by-id"),
    path('product/<int:id>/review/', ProductReviewView.as_view(), name="product-review"),
]
