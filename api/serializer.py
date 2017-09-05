import base64
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.files.base import ContentFile
from django.utils import six
from rest_framework import serializers, exceptions
from rest_framework.generics import get_object_or_404

from users.models import UserProfile
from users.views import search_user

"""Note: Serializing is changing the data from complex querysets from the DB to a form of data we can understand, like 
JSON or XML. Deserializing is reverting this process after validating the data we want to save to the DB."""

"""This class is to parse the image received in JSON format, in Base64 coding, of the mobile app and save it into a 
ImageField.
Note: this is only to download the image from the mobile. """
class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

""" Class to implement the user Serializer that will map the user model into a **kwargs hash o dictionary that will be
converted into a JSON afterward."""
class UserSerializer(serializers.ModelSerializer):

    # Class Meta that define the data of the model that will be converted into a hash or dictionary format, with some
    # property
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'password', 'is_active')
        extra_kwargs = {'username': {'validators': [UnicodeUsernameValidator()], },
                        'password': {'write_only': True},
                        'is_active': {'read_only': True}}

    # Function overridden of the original, that will be used to define the update of one or more attributes in one JSON
    # format instance into a model instance, used in operation related with PUT methods. This function is called by
    # update operation of the UserProfileSerializer because this Serializer is extension of that.
    #
    # @date [31/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/sahidr/CanopyVerdeAPI/blob/master/API/serializers.py]
    #
    # @param [UserSerializer object] self It is a instance or object of this class.
    #
    # @param [User object] instance Instance corresponding to the model that will be updated.
    #
    # @param [Validator] validate_data It is a validator of this class data
    #
    # @returns [User object]
    def update(self, instance, validated_data):
        email = validated_data['email']
        user = User.objects.filter(email=email)
        if user is None:
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)

        password = validated_data['password']

        if (len(str(password)) >= 8):
            instance.set_password(password)
        instance.save()
        return instance


"""Class to implement the user profile Serializer that will map the UserProfile model into a **kwargs hash o dictionary 
that will be converted into a JSON afterward. """
class UserProfileSerializer(serializers.ModelSerializer):

    # This will link the user serializer instance with the UserProfile fk
    user_fk = UserSerializer()

    # This will parse the image in Base64 to a ImageField
    image_profile = Base64ImageField(
        max_length=None, required=False, use_url=True,
    )

    # Class Meta that define the data of the model that will be converted into a hash or dictionary format, with some
    # property
    class Meta:
        model = UserProfile
        fields = ('user_fk', 'phone', 'image_profile', 'address', 'points_accumulated', 'badge_acquired')

    # Function overridden of the original, that will be used to define the creation of one JSON format instance into a
    # model instance, used in operation related with the POST methods.
    #
    # @date [30/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/sahidr/CanopyVerdeAPI/blob/master/API/serializers.py]
    #
    # @param [UserProfileSerializer object] self It is a instance or object of this class.
    #
    # @param [Validator] validate_data It is a validator of this class data
    #
    # @returns [UserProfile object]
    def create(self, validated_data):
        user_data = validated_data.pop('user_fk')
        email = user_data['email']
        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError("User already created")
        else:
            new_user = User(username=user_data['username'], email=email, first_name=user_data['first_name'])
            new_user.set_password(user_data['password'])
            new_user.save()
            user_profile = UserProfile.objects.create(user_fk=new_user, **validated_data)
            return user_profile

    # Function overridden of the original, that will be used to define the update of one or more attributes in one JSON
    # format instance into a model instance, used in operation related with PUT methods. This function will call the
    # update operation of the UserSerializer because this Serializer extend of that.
    #
    # @date [31/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/sahidr/CanopyVerdeAPI/blob/master/API/serializers.py]
    #
    # @param [UserProfileSerializer object] self It is a instance or object of this class.
    #
    # @param [UserProfile object] instance Instance corresponding to the model that will be updated.
    #
    # @param [Validator] validate_data It is a validator of this class data
    #
    # @returns [UserProfile object]
    def update(self, instance, validated_data):
        # A instance of a profile will be updated

        # This will obtain the user data and call the UserSerializer to update its instance.
        user_data = validated_data.pop('user_fk')
        username = self.data['user_fk']['username']
        user = User.objects.get(username=username)
        user_serializer = UserSerializer(data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)

        # This will update the fields that corresponding to the UserProfile instance.
        instance.image_profile = validated_data.get('image_profile', instance.image_profile)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance

"""Class to implement the user Auth Custom Token Serializer that will map the User and UserProfile model with their 
key_activation or token field, and save its, to processing the authentication of the user that is using the TimePiece 
App, into a  **kwargs hash o dictionary that will be converted into a JSON afterward."""
class AuthCustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # Function overridden of the original, that will be used to validate the fields defined in this Serializer.
    #
    # @date [31/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/sahidr/CanopyVerdeAPI/blob/master/API/serializers.py]
    #
    # @param [UserProfileSerializer object] self It is a instance or object of this class.
    #
    # @param [User object] attrs Object that handler the attributes of the instance belong to User model.
    #
    # @returns [User object]
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Maybe this check is unnecessary because this search is for the case in the user introduce a username or a
            # email, and it want to obtain the user associated. But by lack of time, this will be analyze in the future,
            # because affect the design.
            if search_user(username):
                user_request = get_object_or_404(
                    User,
                    email=username,
                )
                username = user_request.username

            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = "User account is disabled."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to log in with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must include email or username and password"
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs