from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, renderers
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import UserSerializer, UserProfileSerializer, AuthCustomTokenSerializer
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

# This class permit to receive the LogIn request of the TimePiece App, verify the credentials with the
# AuthCustomTokenSerializer, generate a token and return the response with the data corresponding.
class LogInView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    # Function that received the authentication post from the TimePiece App, verify the data, generate the token, and
    # generate the response content in a success case, and return its.
    #
    # @date [31/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/sahidr/CanopyVerdeAPI/blob/master/API/views.py]
    #
    # @param [LogInView objects] self Represent the LogInView object associated.
    #
    # @param [HttpRequest] request Request of the App.
    #
    # @returns [HttpResponse]
    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_profile = UserProfile.objects.get(user_fk=user.pk)
        user_profile.key_activation = str(token)
        user_profile.save()

        """
            Content of the Response after successful login
        """
        content = {
            'id': user.pk,
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'first_name': user_profile.first_name,
            'phone': user_profile.phone,
            'address': user_profile.address,
        }
        return Response(content)
