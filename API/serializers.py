from rest_framework import serializers
from ST_App.models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"