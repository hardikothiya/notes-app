from django.urls import path
from .views import NoteListCreateView, NoteDetailView, UserRegistrationView, NoteVersionHistoryView, UserLoginView,NoteShareView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('notes/create/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/version-history/<int:pk>/', NoteVersionHistoryView.as_view(), name='note-version-history'),
    path('notes/share/<int:pk>/', NoteShareView.as_view(), name='note-share'),

]
