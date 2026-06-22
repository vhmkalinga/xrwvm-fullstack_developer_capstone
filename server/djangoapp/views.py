from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    """Handles user sign-in and authentication requests."""
    # Get username and password from request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Try to check if provided credentials can be authenticated
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    
    if user is not None:
        # If user is valid, call login method to log in current user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
        
    return JsonResponse(response_data)


@csrf_exempt
def logout_request(request):
    """Handles user sign-out and session termination requests."""
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username as confirmation
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    """Handles new user signup requests, saves credentials, and initiates session login."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    
    username_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        # If not, log that this is a new user
        logger.debug("{} is a new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            email=email
        )
        # Login the user immediately
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(response_data)
    else:
        response_data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(response_data)


# # Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request, dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...