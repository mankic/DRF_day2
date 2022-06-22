
from django.contrib import admin
from django.urls import path, include
from product import views

urlpatterns = [
    # product/     # CBV 는 .as_view() 추가해줘야함
    path('', views.ProductView.as_view()),
    path('<product_id>/', views.ProductView.as_view()),
]
