from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

class NoteChange(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='version_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()
    added_content = models.TextField()  

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
