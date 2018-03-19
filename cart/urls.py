from django.urls import path
from cart import views

urlpatterns = [
    path('', views.show_cart, name='cart',),

]
