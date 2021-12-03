import logging
from datetime import datetime, timezone

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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

    # Check if password confirmation matches
    logging.debug(f"Checking if password is the same as confirmation")
    if password != confirm:
        return JsonResponse({"success": False, "messages": ["Passwords did not match"]})

    # Check if user with that email already exists
    try:
        logging.debug(f"Checking if user already exists")
        if EmailUser.objects.get(email=email):
            return JsonResponse({"success": False, "messages": ["User with that email already exists."]})
    except ObjectDoesNotExist:
        pass

    # Create User
    logging.debug(f"Creating user with email {email}")
    user = EmailUser.objects.create_user(email=email, password=password)

    if user is None:
        return JsonResponse({"success": False, "messages": ["Error with user creation, please try again later"]})

    # Log user in a redirect to dashboard
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

    return render(request, "dashboard.html", {"keys": list(zip(status_list, apiKeys))})


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


@login_required(login_url="revoke_key")
def revoke_key(request):
    if request.method != "POST":
        return JsonResponse({"messages": [f"Method {request.method} not allowed."]})

    key = UserAPIKey.objects.get(id=request.POST["key"])
    key.revoked = True
    key.save()

    return JsonResponse({"redirect": reverse("dashboard")})
