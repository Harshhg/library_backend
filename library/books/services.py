from django.utils import timezone
from rest_framework.exceptions import ValidationError
from library.books.models import Book, IssuedBook
from library.users.services import get_user_remaining_book_issue_limit


def get_book_ids_issued_by_user(user):
    return user.issued_books.filter(returned_date__isnull=True).values_list("book_id", flat=True)


def get_books_issued_by_user(user):
    book_ids = get_book_ids_issued_by_user(user)
    queryset = Book.objects.filter(id__in=book_ids)
    return queryset


def search_book_by_name(book_name):
    return Book.objects.filter(name__icontains=book_name)


def issue_book_to_user(book, user):
    issued_books = get_book_ids_issued_by_user(user)
    if not get_user_remaining_book_issue_limit(user):
        raise ValidationError("Sorry you already have issued maximum books")

    if book.id in issued_books:
        raise ValidationError("Book is already issued to you")

    IssuedBook.objects.create(user=user, book=book)
    book.is_available = False
    book.save()


def return_book_from_user(book):
    IssuedBook.objects.filter(book=book).update(returned_date=timezone.now())
    book.is_available = True
    book.save()

