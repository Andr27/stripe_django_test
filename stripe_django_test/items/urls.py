from django.urls import path
from . import views
urlpatterns = [
    path('buy/<int:id>/', views.buy, name='buy_item'),
    path('item/<int:id>/', views.item, name='item'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy-order/<int:order_id>/', views.buy_order, name='buy_order'),
]
