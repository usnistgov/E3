import logging
from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.models import UserAPIKey, EmailUser

# Create your views here.

logger = logging.getLogger(__name__)


def email_login(request):
    logout(request)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({"redirect": reverse("dashboard")})
        else:
            return JsonResponse({"messages": ["Username or password incorrect. please try again."]})

    return render(request, "login.html")


def register(request):
    if request.method != "POST":
        return JsonResponse({"errors": f"Method {request.method} not allowed."})

    logger.info("register user")

    email = request.POST["email"]
    password = request.POST["password"]
    confirm = request.POST["confirm-password"]

    if password != confirm:
        return JsonResponse({"success": False, "messages": ["Passwords did not match"]})

    user = EmailUser.objects.create_user(email=email, password=password)

    if user is None:
        return JsonResponse({"success": False, "messages": ["Error with user creation, please try again later"]})

    user = authenticate(email=email, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return JsonResponse({"redirect": reverse("dashboard")})


@login_required(login_url="login")
def dashboard(request):
    apiKeys = UserAPIKey.objects.all().filter(user=request.user.id)
    status_list = ["active"] * len(apiKeys)

    if request.method == "POST":
        keyName = request.POST["name"]
        keyExpiryDate = request.POST["expire-datetime"]

        keyExpiryDate = datetime.strptime(keyExpiryDate, "%Y-%m-%dT%H:%M") if keyExpiryDate else None

        name, newKey = UserAPIKey.objects.create_key(user=request.user, name=keyName, expiry_date=keyExpiryDate)

        return JsonResponse({"name": str(name), "key": str(newKey)})

    for index, apiKey in enumerate(apiKeys):
        if apiKey.revoked:
            status_list[index] = "revoked"
        elif apiKey.expiry_date is not None and datetime.now(timezone.utc) > apiKey.expiry_date:
            status_list[index] = "expired"

    return render(request, "dashboard.html", {"keys": zip(status_list, apiKeys)})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def delete_user(request):
    if request.method != "POST":
        return JsonResponse({"messages": [f"Method {request.method} not allowed."]})

    if not request.user.check_password(request.POST["password-confirm"]):
        return JsonResponse({"messages": ["Password incorrect"]})

    EmailUser.objects.get(id=request.user.id).delete()
    return JsonResponse({"redirect": reverse("login")})
