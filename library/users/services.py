from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from rest_framework import exceptions
from library.users.models import User


def generate_token():
    token_length = settings.USER_EMAIL_VERIFICATION.get("TOKEN_LENGTH")
    token = get_random_string(length=token_length)
    return token


def create_user_account(**kwargs):
    user = User.objects.create_user(username=kwargs.get("email"), **kwargs)
    return user


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise exceptions.NotAuthenticated("Invalid username/password. Please try again!")
    if not user.is_verified():
        raise exceptions.AuthenticationFailed("User is not verified !")
    return user


# todo: cache this function
def get_user_remaining_book_issue_limit(user):
    issued_books_ids = user.issued_books.filter(returned_date__isnull=True).values_list("book_id", flat=True)
    return settings.MAX_BOOK_ISSUE_COUNT_PER_USER - len(issued_books_ids)