from rest_framework import serializers
from .models import Rebate

class RebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rebate
        fields = '__all__'
