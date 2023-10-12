from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count', 'get_authors')
    list_filter = ('count', 'name')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'date_of_release')
        }),
        ('Availability', {
            'fields': ('count', 'date_of_issue')
        })
    )

    def get_authors(self, obj):
        return ", ".join([f'{author.name} {author.surname} {author.patronymic}' for author in obj.authors.all()])

    get_authors.short_description = 'Authors'


admin.site.register(Book, BookAdmin)