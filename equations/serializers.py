from rest_framework import serializers
from .models import Mathematician, Equation

#serializers convert models (db format) into JSON format to allow API usage

class MathematicianSerializer(serializers.ModelSerializer):
    class Meta: #meta is an inner class whihc allows more control over customizability, in serializers specifying the model associated + fields
        model = Mathematician
        fields = '__all__'

class EquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equation
        fields = '__all__'