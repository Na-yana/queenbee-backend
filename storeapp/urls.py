from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, CategoryViewSet, create_order, verify_payment, get_category_offer

router=routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns=[
    path('', include(router.urls)),
    path('create-order/', create_order),
    path('verify-payment/', verify_payment),
    path('category-offer/<int:category_id>/', get_category_offer),
]

