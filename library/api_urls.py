from rest_framework.routers import DefaultRouter

from library.books.apis import BookViewSet
from library.users.apis import AuthViewSet, CurrentUserViewSet

default_router = DefaultRouter(trailing_slash=False)

default_router.register("auth", AuthViewSet, basename="auth")
default_router.register("me", CurrentUserViewSet, basename="books")
default_router.register("books", BookViewSet, basename="books")


urlpatterns = default_router.urls


