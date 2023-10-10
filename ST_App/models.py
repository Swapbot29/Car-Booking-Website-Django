from django.db import models

# Create your models here.

class Car(models.Model):
    car_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    year = models.IntegerField()
    number_of_seats = models.IntegerField()
    cost_per_day = models.CharField(max_length=10)
    cost_for_outstation = models.CharField(max_length=10, null=True)

    car_image = models.ImageField(upload_to='car_images/')  # Define the upload_to path as per your needs

    def __str__(self):
        return f"{self.year} {self.company_name} {self.car_name}"
    
class User_booking(models.Model):
    car_name = models.ForeignKey(Car, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    address = models.TextField()
    date = models.DateTimeField()
    to = models.DateTimeField()

    def __str__(self):
        return f"{self.user_name} - {self.car_name} - {self.date}"
    
class PrivateMsg(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()