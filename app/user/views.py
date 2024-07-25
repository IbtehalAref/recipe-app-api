"""

Views for user API.
"""

from rest_framework import generics
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