from rest_framework import serializers
from .models import TCL,Iot

class TCLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCL
        fields = '__all__'
class IOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iot
        fields = '__all__'