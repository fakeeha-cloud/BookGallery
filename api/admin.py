from django.contrib import admin

# Register your models here.
from api.models import Book

admin.site.register(Book)