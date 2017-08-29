from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from api.serializer import UserSerializer, UserProfileSerializer
from users.models import UserProfile

"""Note: - The ListCreateAPIView is a generic view which provides GET (list all) and POST method handlers.
         - RetrieveUpdateDestroyAPIView is a generic view that provides GET(one), PUT, PATCH and DELETE method handlers.
"""

# Create your views here.

# This class help to list the users in User model by GET and permit add a new user by POST.
class CreateViewUser(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    """Save the post data when creating a new list of users. In other words method that aids in saving a new user list 
    once posted"""
    def perform_create(self, serializer):
        serializer.save()

# This class help to show the detail of each user of the CreateViewUser by GET(one) and permit modifier some fields by
# PUT, and others characteristic by PATCH and DELETE.
class DetailViewUser(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

# This class help to list the users in UserProfile model by GET and permit add a new user by POST.
class CreateViewUserProfile(generics.ListCreateAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    """Save the post data when creating a new list of users. In other words method that aids in saving a new user list 
        once posted"""
    def perform_create(self, serializer):
        serializer.save()

# This class help to show the detail of each user of the CreateViewUser by GET(one) and permit modifier some fields by
# PUT, and others characteristic by PATCH and DELETE.
class DetailViewUserProfile(generics.RetrieveUpdateDestroyAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer