from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FoodWaste
from .serializers import FoodWasteSerializer
from analytics.mongodb import log_event
class FoodWasteViewSet(viewsets.ModelViewSet):
    serializer_class=FoodWasteSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role=="ADMIN": return FoodWaste.objects.all()
        return FoodWaste.objects.filter(owner=self.request.user)
    def perform_create(self,serializer):
        record=serializer.save(owner=self.request.user)
        log_event("waste_history",{"action":"created","record_id":record.id,"source":record.source,"food_type":record.food_type,"prepared":record.prepared_quantity,"wasted":record.wasted_quantity,"date":str(record.date),"user":self.request.user.username})
    def perform_update(self,serializer):
        record=serializer.save(); log_event("activity_history",{"action":"updated_waste","record_id":record.id,"user":self.request.user.username})
    def perform_destroy(self,instance):
        log_event("activity_history",{"action":"deleted_waste","record_id":instance.id,"user":self.request.user.username}); instance.delete()
