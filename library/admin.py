from django.contrib import admin
from .models import Book, Note, Quote
# Register your models here.

admin.site.register(Book)
admin.site.register(Note)
admin.site.register(Quote)  