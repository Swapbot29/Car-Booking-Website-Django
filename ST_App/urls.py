from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='home'),name='logout'),
    path('register/',views.RegisterPage.as_view(),name='register'),
    path('admin_carlist/',views.AdminCarListView.as_view(), name='admin_carlist'),
    path('export-users-to-excel/', views.ExportUsersToExcelView.as_view(), name='export_users_to_excel'),
    path('', views.HomeView.as_view(),name='home'),
    path('car_list/', views.CarListView.as_view(), name='car_list'),
    path('add-car/', views.AddCarView.as_view(), name='add_car'),
    path('car-detail/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car-update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('car-delete/<int:pk>/', views.CarDeleteView.as_view(), name='car_delete'),
    path('book-car/', views.CarBooking.as_view(), name='book_car'),
    path('booking-list/', views.order_list.as_view(), name='book_list'),
    path('booking-detail/<int:pk>/', views.BookingDetail.as_view(), name='book_detail'),
    path('booking-update/<int:pk>/', views.BookingUpdate.as_view(), name='booking_update'),
    path('booking/delete/<int:pk>/', views.BookingDeleteView.as_view(), name='booking_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)