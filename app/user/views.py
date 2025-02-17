"""

Views for user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    userSerializer,
    AuthTokenSerializar
)


class CreateUserView(generics.CreateAPIView):

    """Create a new user in system."""

    serializer_class = userSerializer


class CreateTokenview(ObtainAuthToken):

    serializer_class = AuthTokenSerializar
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user."""

    serializer_class = userSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """return and retrieve the authenticated user"""
        return self.request.user
