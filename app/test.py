from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note

class NoteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_create_note(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/notes/create/', {'content': 'Test note content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)

    def test_get_note(self):
        note = Note.objects.create(content='Test note content', owner=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test note content')

    def test_unauthenticated_user_cannot_create_note(self):
        response = self.client.post('/api/notes/create/', {'content': 'Unauthorized content'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Note.objects.count(), 0)

    def test_update_note(self):
        note = Note.objects.create(content='Original content', owner=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/api/notes/{note.id}/', {'content': 'Updated content'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.get(id=note.id).content, 'Original content\nUpdated content')

    def test_share_note(self):
        note = Note.objects.create(content='Post for share', owner=self.user)
        self.client.force_authenticate(user=self.user)
        user = User.objects.create_user(username='shareduser', password='testpassword')
        response = self.client.post(f'/api/notes/share/{note.id}/', {"users" :[user.id]})
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

