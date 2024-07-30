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
    path('products/popular/', ProductsPopularView.as_view(), name="products-popular"),
    path('products/limited/', ProductsLimitedView.as_view(), name="products-limited"),
    path('sales', SalesView.as_view(), name="sales"),  # fix
    path('banners/', BannersView.as_view(), name="banners"),  # fix
    path('basket', BasketView.as_view(), name="basket"),
    path('orders', OrdersView.as_view(), name="orders"),
    path('order/<int:id>', OrdersByIdView.as_view(), name="order-by-id"),
    path('payment/<int:id>', PaymentView.as_view(), name="payment-by-id"),
    path('tags/', TagsView.as_view(), name="tags"),
    path('product/<int:id>', ProductByIdView.as_view(), name="product-by-id"),
    path('product/<int:id>/reviews', ProductReviewView.as_view(), name="product-review"),
]
