from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Donation, Collection
from .serializers import DonationSerializer
from analytics.mongodb import log_event

class DonationViewSet(viewsets.ModelViewSet):
    serializer_class = DonationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ["ADMIN", "NGO"]:
            return Donation.objects.all()
        return Donation.objects.filter(provider=user)

    def perform_create(self, serializer):
        item = serializer.save(provider=self.request.user)
        log_event("activity_history", {"action":"donation_created", "donation_id":item.id, "user":self.request.user.username})

    @action(detail=True, methods=["post"])
    def claim(self, request, pk=None):
        if request.user.role != "NGO" and not request.user.is_staff:
            return Response({"detail":"Only NGOs or volunteers can claim donations."}, status=403)
        donation = self.get_object()
        if donation.status != "AVAILABLE":
            return Response({"detail":"This donation is not available."}, status=400)
        donation.status = "CLAIMED"
        donation.save()
        Collection.objects.create(donation=donation, volunteer=request.user)
        log_event("collection_history", {"action":"claimed", "donation_id":donation.id, "volunteer":request.user.username})
        return Response(DonationSerializer(donation).data)

    @action(detail=True, methods=["post"])
    def collect(self, request, pk=None):
        donation = self.get_object()
        collection, _ = Collection.objects.get_or_create(donation=donation)
        if collection.volunteer != request.user and not request.user.is_staff:
            return Response({"detail":"Only the assigned volunteer can mark this donation collected."}, status=403)
        donation.status = "COLLECTED"
        donation.save()
        collection.collected_at = timezone.now()
        collection.save()
        log_event("collection_history", {"action":"collected", "donation_id":donation.id, "user":request.user.username})
        return Response(DonationSerializer(donation).data)
