from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages

from library.books.models import Book, IssuedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "serial_no", "name", "author", "price", "edition", "is_available", "issued_to"]
    list_filter = ["is_available"]
    readonly_fields = ["issued_to"]
    search_fields = ["name", "serial_no", "author", "edition"]
    actions = ['delete_selected']

    def issued_to(self, book):
        issued_book = IssuedBook.objects.filter(book=book).order_by("-borrowed_date").first()
        if not issued_book or issued_book.returned_date is not None:
            return "-"

        user = issued_book.user
        user_url = reverse('admin:%s_%s_change' % ("users", "user"), args=[user.id])
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            user_url,
            f"{user.first_name} {user.last_name}"
        )

    def save_model(self, request, obj, form, change):
        if IssuedBook.objects.filter(book=obj, returned_date__isnull=True).exists():
            messages.warning(request, f"Cannot Update {obj} because this book is issued.")
            return
        super().save_model(request, obj, form, change)

    def delete_selected(self, request, queryset):
        issued_books = IssuedBook.objects.filter(returned_date__isnull=True).values_list("book_id", flat=True)
        for obj in queryset:
            if obj.id in issued_books:
                messages.warning(request, f"Cannot delete {obj} because this book is issued.")
            else:
                obj.delete()
                self.message_user(request, f"{queryset.count()} object(s) were deleted.")

    delete_selected.short_description = "Delete selected Books"
