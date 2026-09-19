from rest_framework import serializers
from .models import Donation, Collection

class DonationSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="provider.username", read_only=True)
    collection_volunteer = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = ("id", "provider", "provider_name", "collection_volunteer", "food_name", "quantity", "pickup_address", "available_until", "status", "created_at")
        read_only_fields = ("provider", "created_at")

    def get_collection_volunteer(self, obj):
        return obj.collection.volunteer.username if hasattr(obj, "collection") and obj.collection.volunteer else None

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ("volunteer",)
