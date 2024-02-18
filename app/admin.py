from django.contrib import admin
from .models import SharedNote, Note, NoteChange


admin.site.register(SharedNote)
admin.site.register(Note)
admin.site.register(NoteChange)
