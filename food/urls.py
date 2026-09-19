from rest_framework.routers import DefaultRouter
from .views import FoodWasteViewSet
router=DefaultRouter(); router.register("waste",FoodWasteViewSet,basename="waste")
urlpatterns=router.urls
