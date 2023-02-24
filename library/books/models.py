from django.db import models
from library.users.models import User


class Book(models.Model):
    serial_no = models.CharField(unique=True, max_length=120)
    name = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    edition = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)


class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issued_by")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issued_books")
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True)
