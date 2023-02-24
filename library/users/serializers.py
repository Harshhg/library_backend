import base64

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from library.books.serializers import BookListSerializer
from library.books.services import get_books_issued_by_user
from library.users.models import User
from library.users.services import get_user_remaining_book_issue_limit


class UserSerializer(serializers.ModelSerializer):
    issued_books = serializers.SerializerMethodField()
    verification_id = serializers.SerializerMethodField()
    remaining_limit = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "remaining_limit", "issued_books", "verification_id"]

    def get_verification_id(self, user):
        return base64.b64encode(user.verification_id.data) if user.verification_id else ""

    def get_remaining_limit(self, user):
        return get_user_remaining_book_issue_limit(user)

    def get_issued_books(self, user):
        books_queryset = get_books_issued_by_user(user)
        if not books_queryset:
            return []

        self.context["request"].user = user
        return BookListSerializer(books_queryset, context=self.context, many=True).data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "password",
            "email",
            # "verification_id"
        ]
        # extra_kwargs = {
        #     "verification_id": {"required": True}
        # }


class AuthUserSerializer(UserSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ["auth_token"] + UserSerializer.Meta.fields

    def get_auth_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
