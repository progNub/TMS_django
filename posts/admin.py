from django.contrib import admin

from posts.models import Note


# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Note, NoteAdmin)