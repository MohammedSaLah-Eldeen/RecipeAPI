"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import *


class CreateUserView(generics.CreateAPIView):
    """creates a new user in the system.

       Thie generic class comes with preconfigured way
       to handle POST requests.
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classses = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manages the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieves and return the authenticated user."""
        return self.request.user