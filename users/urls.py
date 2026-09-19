# from django.urls import path
# from . import views
# urlpatterns=[
#     path("register/",views.register),
#     path("login/",views.user_login),
#     path("logout/",views.user_logout),
#     path("me/",views.profile)
# ]


from django.urls import path
from django.http import JsonResponse
from . import views

def users_home(request):
    return JsonResponse({
        "message": "Users API is working"
    })

urlpatterns = [
    path("", users_home),
    path("register/", views.register),
    path("login/", views.user_login),
    path("logout/", views.user_logout),
    path("me/", views.profile)
]