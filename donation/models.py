from django.conf import settings
from django.db import models
class Donation(models.Model):
    class Status(models.TextChoices): AVAILABLE="AVAILABLE","Available"; CLAIMED="CLAIMED","Claimed"; COLLECTED="COLLECTED","Collected"; EXPIRED="EXPIRED","Expired"
    provider=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="donations")
    food_name=models.CharField(max_length=100)
    quantity=models.FloatField(help_text="Quantity in kilograms")
    pickup_address=models.CharField(max_length=255)
    available_until=models.DateTimeField()
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.AVAILABLE)
    created_at=models.DateTimeField(auto_now_add=True)
class Collection(models.Model):
    donation=models.OneToOneField(Donation,on_delete=models.CASCADE,related_name="collection")
    volunteer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    collected_at=models.DateTimeField(null=True,blank=True)
    notes=models.TextField(blank=True)
