from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer

@ensure_csrf_cookie
@login_required
def dashboard(request):
    if request.user.is_staff or request.user.role == "ADMIN":
        return redirect("admin-dashboard")
    if request.user.role == "NGO":
        return redirect("ngo-dashboard")
    return redirect("provider-dashboard")

@ensure_csrf_cookie
@login_required
def provider_dashboard(request):
    if request.user.role not in ["PROVIDER", "ADMIN"] and not request.user.is_staff:
        return HttpResponseForbidden("This dashboard is for food providers.")
    return render(request, "provider_dashboard.html")

@ensure_csrf_cookie
@login_required
def ngo_dashboard(request):
    if request.user.role not in ["NGO", "ADMIN"] and not request.user.is_staff:
        return HttpResponseForbidden("This dashboard is for NGOs and volunteers.")
    return render(request, "ngo_dashboard.html")

@ensure_csrf_cookie
@login_required
def admin_dashboard(request):
    if not (request.user.is_staff or request.user.role == "ADMIN"):
        return HttpResponseForbidden("This dashboard is for administrators.")
    return render(request, "admin_dashboard.html")

@ensure_csrf_cookie
def food_page(request): return render(request, "food.html")
@ensure_csrf_cookie
def analytics_page(request): return render(request, "analytics.html")
@ensure_csrf_cookie
def login_page(request): return render(request, "login.html")
@ensure_csrf_cookie
def register_page(request): return render(request, "register.html")

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        return Response(UserSerializer(serializer.save()).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    user = authenticate(request, username=request.data.get("username"), password=request.data.get("password"))
    if not user: return Response({"detail": "Invalid username or password."}, status=400)
    login(request, user)
    return Response({"message": "Logged in", "username": user.username, "role": user.role})

@api_view(["POST"])
def user_logout(request): logout(request); return Response({"message": "Logged out"})
@api_view(["GET"])
def profile(request): return Response({"username": request.user.username, "role": request.user.role, "is_staff": request.user.is_staff})
