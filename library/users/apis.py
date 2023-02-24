# Third Party Stuff
import base64

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from library.assets.services import save_verification_id
from library.users.models import User
from library.users.serializers import AuthUserSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from library.users.services import create_user_account, get_and_authenticate_user


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.pop("email", None)
        user = get_and_authenticate_user(email=email, **serializer.validated_data)
        response_serializer = AuthUserSerializer(
            user, context=self.get_serializer_context()
        )
        return Response(response_serializer.data)

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_id = request.FILES.get("verification_id", None)

        if not verification_id:
            raise ValidationError("Verification ID is required !")

        image = save_verification_id(verification_id)
        serializer.validated_data["verification_id"] = image

        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data)


class CurrentUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        data = UserSerializer(request.user, context=self.get_serializer_context()).data
        return Response(data)