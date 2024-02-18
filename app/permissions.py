from rest_framework import permissions
from .models import SharedNote
class HasAccessToNote(permissions.BasePermission):
    def has_permission(self, request, view):
        note = view.get_object()  
        return request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists()
