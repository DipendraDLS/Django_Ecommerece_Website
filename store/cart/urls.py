from . import views
from django.urls import path

urlpatterns = [
    path('', views.cart, name='cart'),
    path('cart_quantity',views.cart_quantity,name='cart_quantity'),
    path('get_cart_price_details', views.get_cart_price_details),
    path('change_cart_quantity', views.change_cart_quantity),
    path('add_to_cart/<int:id>/<int:quantity>', views.add_to_cart, name='add_to_cart'),
    path('delete_cart/<int:id>/<int:flag>', views.delete_cart, name='delete_cart'),
    # path('', views.ListCart, name='list-carts'),
    path('item/<int:pk>/', views.DetailCart.as_view(), name='detail-cart'),
    path('create/<int:id>', views.CreateCart.as_view(), name='create-cart'),
    path('<int:pk>/update/', views.Updatecart.as_view(), name='update-cart'),
    path('<int:pk>/delete/', views.DeleteCart.as_view(), name='delete-cart'),
]