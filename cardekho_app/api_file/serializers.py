from rest_framework import serializers
from ..models import Carlist

def alphanumeric(value):
    if not str(value).isalnum():
        raise serializers.ValidationError("Name can have number or character no special characters")

class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name =serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(read_only=True)
    chassisnumber = serializers.CharField(validators=[alphanumeric])
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    def create(self,validated_data):
        return Carlist.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.active = validated_data.get('active',instance.active)
        instance.chassisnumber = validated_data.get('chassisnumber',instance.chassisnumber)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance
    
    def validate_price(self, value):
        if value <= 20000.00:
            raise serializers.ValidationError("Price is too low")
        return value
    
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("name and description cannot be same")
        return data