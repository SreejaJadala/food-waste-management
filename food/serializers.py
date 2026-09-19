from rest_framework import serializers
from .models import FoodWaste
class FoodWasteSerializer(serializers.ModelSerializer):
    class Meta: model=FoodWaste; fields=("id","source","food_type","prepared_quantity","wasted_quantity","date","created_at"); read_only_fields=("id","created_at")
    def validate(self,data):
        if data.get("wasted_quantity",0)>data.get("prepared_quantity",0): raise serializers.ValidationError("Wasted quantity cannot be greater than prepared quantity.")
        return data
