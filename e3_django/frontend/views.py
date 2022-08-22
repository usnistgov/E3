import logging
from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from frontend.models import UserAPIKey, EmailUser

# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


def email_login(request):
    logout(request)

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        logging.info(f"Attempting login of user {email}")

        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            messages.warning(request, "Username or password incorrect. Please try again.")

    return render(request, "login.html")


def register(request):
    if request.method != "POST":
        return messages.error(request, f"Method {request.method} not allowed.")

    email = request.POST["email"]
    password = request.POST["password"]
    confirm = request.POST["confirm-password"]

    logger.info(f"Attempting to register user with name: {email}")

    # Check if password confirmation matches
    logging.debug(f"Checking if password is the same as confirmation")
    if password != confirm:
        return messages.warning(request, "Passwords did not match")

    # Check if user with that email already exists
    try:
        logging.debug(f"Checking if user already exists")
        if EmailUser.objects.get(email=email):
            return messages.warning(request, "User with that email already exists.")
    except ObjectDoesNotExist:
        pass

    # Create User
    logging.debug(f"Creating user with email {email}")
    user = EmailUser.objects.create_user(email=email, password=password)

    if user is None:
        return messages.error(request, "Error with user creation, please try again later.")

    # Log user in a redirect to dashboard
    user = authenticate(email=email, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return redirect(reverse("dashboard"))


@login_required(login_url="login")
def dashboard(request):
    api_keys = UserAPIKey.objects.all().filter(user=request.user.id)
    status_list = ["active"] * len(api_keys)

    if request.method == "POST":
        key_name = request.POST["name"]
        key_expiry_date = request.POST["expire-datetime"]

        logging.debug(f"Attempting to create key with name: {key_name}")

        key_expiry_date = datetime.strptime(key_expiry_date, "%Y-%m-%dT%H:%M") if key_expiry_date else None

        name, new_key = UserAPIKey.objects.create_key(user=request.user, name=key_name, expiry_date=key_expiry_date)

        return JsonResponse({"name": str(name), "key": str(new_key)})

    for index, apiKey in enumerate(api_keys):
        if apiKey.revoked:
            status_list[index] = "revoked"
        elif apiKey.expiry_date is not None and datetime.now(timezone.utc) > apiKey.expiry_date:
            status_list[index] = "expired"

    return render(request, "dashboard.html", {"keys": list(zip(status_list, api_keys))})


@login_required(login_url="login")
def logout_view(request):
    logging.debug(f"Attempting to log out user: {getattr(request, 'user', None)}")
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def delete_user(request):
    if request.method != "POST":
        return JsonResponse({"messages": [f"Method {request.method} not allowed."]})

    if not request.user.check_password(request.POST["password-confirm"]):
        return JsonResponse({"messages": ["Password incorrect"], "variant": "warning"})

    logging.debug(f"Attempting to delete user: {request.user}")
    EmailUser.objects.get(id=request.user.id).delete()
    return JsonResponse({"redirect": reverse("login")})


@login_required(login_url="revoke_key")
def revoke_key(request):
    if request.method != "POST":
        return JsonResponse({"messages": [f"Method {request.method} not allowed."]})

    logging.debug(f"Attempting to revoke key: {request.POST['key']}")

    key = UserAPIKey.objects.get(id=request.POST["key"])
    key.revoked = True
    key.save()

    return JsonResponse({"redirect": reverse("dashboard")})
