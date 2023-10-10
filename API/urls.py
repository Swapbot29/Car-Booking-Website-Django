from django.urls import path
from .views import CarListAPIView, CarUpdateViews, CarDeleteViews, CarDetailView
# from rest_framework.authtoken import views

urlpatterns = [
    path('',CarListAPIView.as_view(),name='car_list_api'),
    path('update-car/<int:pk>/',CarUpdateViews.as_view(),name='update-car'),
    path('car-update/<int:id>',CarUpdateViews.as_view(),name='car-update'),
    path('car-delete/<int:id>',CarDeleteViews.as_view(),name='car-delete'),
]