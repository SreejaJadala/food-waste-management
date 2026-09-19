from django.contrib import admin
from django.urls import include, path
from users import views
urlpatterns = [
    path("admin/", admin.site.urls), path("", views.dashboard, name="dashboard"),
    path("dashboard/provider/", views.provider_dashboard, name="provider-dashboard"),
    path("dashboard/ngo/", views.ngo_dashboard, name="ngo-dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin-dashboard"),
    path("food/", views.food_page), path("analytics/", views.analytics_page),
    path("login/", views.login_page), path("register/", views.register_page),
    path("api/users/", include("users.urls")), path("api/food/", include("food.urls")),
    path("api/donations/", include("donation.urls")), path("api/analytics/", include("analytics.urls")),
]
