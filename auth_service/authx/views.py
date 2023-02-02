from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response

from .jwt import create_jwt

User = get_user_model()


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(_('User not found!'))

        if not user.check_password(password):
            raise AuthenticationFailed(_('Incorrect password!'))

        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }

        token = create_jwt(payload)
        return Response({'jwt': token})


class ActivationUserEmailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(_('Email activation was successfully completed. Now you can log in to your account.'), status=HTTP_204_NO_CONTENT)
        else:
            return Response(_('Email activation error - invalid activation link!'), status=HTTP_204_NO_CONTENT)


class CheckPermissionView(APIView):
    """Check if user has Owner role"""

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role == 4)
        return Response({"permission": perm})


class CheckBaristaPermissionView(APIView):
    """Check if user has Barista role"""

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 2)
        return Response({"permission": perm})


class CheckCashierPermissionView(APIView):
    """Check if user has Cashier role"""

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 1)
        return Response({"permission": perm})


class CheckManagerPermissionView(APIView):
    """Check if user has Manager role"""

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role >= 3)
        return Response({"permission": perm})


class CheckOwnerPermissionView(APIView):
    """Check if user has Owner role"""

    def get(self, request, format=None):
        perm = bool(request.user.is_authenticated and request.user.role == 4)
        return Response({"permission": perm})


class MenuPermissionView(APIView):
    """Check MenuPermission"""

    def get(self, request, format=None):
        permission = bool(
            request.user.is_authenticated and request.user.role >= 1)
        permission_2 = bool(
            request.user.is_authenticated and request.user.role >= 2)
        return Response({
            "has_permission": {
                "retrieve": permission,
                "list": permission,
            },
            "has_object_permission": {
                "retrieve": permission,
                "update": permission_2,
                "partial_update": permission_2,
                "destroy": permission_2,
                "create": permission_2,
            }
        })
