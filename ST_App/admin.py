from django.contrib import admin
from .models import Car, User_booking, PrivateMsg

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ("car_name", "car_image", "company_name")
class OrderAdmin(admin.ModelAdmin):
    list_display = ("car_name", "date", "to")


admin.site.register(Car, CarAdmin)
admin.site.register(User_booking, OrderAdmin)
admin.site.register(PrivateMsg)