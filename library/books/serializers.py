from rest_framework import serializers
from library.books.models import Book, IssuedBook


class BookListSerializer(serializers.ModelSerializer):
    last_issued_on = serializers.SerializerMethodField()
    last_returned_on = serializers.SerializerMethodField()
    is_issued = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "serial_no", "name", "author", "price", "edition", "is_available", "is_issued", "last_issued_on", "last_returned_on"]

    def get_is_issued(self, book):
        user = self.context["request"].user
        return IssuedBook.objects.filter(user=user, book=book, returned_date__isnull=True).exists()

    def get_last_issued_on(self, book):
        user = self.context["request"].user
        issued_book = IssuedBook.objects.filter(user=user, book=book).order_by("-borrowed_date").first()
        return issued_book.borrowed_date if issued_book else None

    def get_last_returned_on(self, book):
        user = self.context["request"].user
        issued_book = IssuedBook.objects.filter(user=user, book=book).order_by("-returned_date").first()
        return issued_book.returned_date if issued_book else None