# from django.contrib import admin
# from .models import Contact


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'description', 'email')

# core/admin.py
from django.contrib import admin
from core.models import Word

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word',)
