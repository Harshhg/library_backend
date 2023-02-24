# Third Party Stuff
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from library.books.models import Book
from library.books.serializers import BookListSerializer
from library.books.services import search_book_by_name, issue_book_to_user, return_book_from_user


class BookViewSet(viewsets.GenericViewSet):
    queryset = Book.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "issue":
            queryset = queryset.filter(is_available=True)

        if self.action == "submit":
            queryset = queryset.filter(issued_by__user=self.request.user, issued_by__returned_date__isnull=True)

        return queryset

    @action(methods=["GET"], detail=False)
    def search(self, request, *args, **kwargs):
        search_param = request.query_params.get("search")
        if not search_param:
            raise ValidationError("'search' query_param is required")

        books = search_book_by_name(search_param)
        response_serializer = BookListSerializer(
            books, context=self.get_serializer_context(), many=True
        )
        return Response(response_serializer.data)

    @action(methods=["POST"], detail=True, url_path="issue")
    def issue(self, request, *args, **kwargs):
        book = self.get_object()
        issue_book_to_user(book, request.user)
        return Response({"success": True})

    @action(methods=["POST"], detail=True)
    def submit(self, request, *args, **kwargs):
        book = self.get_object()
        return_book_from_user(book)
        return Response({"success": True})
