from django.conf import settings
from django.db import models
class FoodWaste(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="waste_records")
    source=models.CharField(max_length=100)
    food_type=models.CharField(max_length=50)
    prepared_quantity=models.FloatField()
    wasted_quantity=models.FloatField()
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-date","-id"]
    def __str__(self): return f"{self.food_type} - {self.date}"
