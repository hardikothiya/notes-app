from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer, NoteSerializer, NoteChangeSerializer, SharedNoteSerializer,NoteVersionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .permissions import HasAccessToNote

from .models import Note, SharedNote, NoteChange

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(username=serializer.validated_data['username']).exists() :
            return Response({'error': 'Username or email already taken'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registration successful'}, status=status.HTTP_201_CREATED, headers=headers)
    

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated,HasAccessToNote]

    def perform_update(self, serializer):

        old_note_instance = self.get_object()
        existing_content = old_note_instance.content

        serializer.save(content=f'{existing_content}\n{serializer.validated_data.get("content", "")}')

        print(serializer.data['content'])
        NoteChange.objects.create(
            note=old_note_instance,
            user=self.request.user,
            changes=serializer.data['content'],
            added_content=serializer.validated_data.get('content', old_note_instance.content)
        )

class NoteVersionHistoryView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteVersionSerializer
    permission_classes = [IsAuthenticated,HasAccessToNote ]

  

class NoteShareView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = SharedNoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != note.owner:
            return Response({'error': 'Unauthorized to share this note'}, status=status.HTTP_403_FORBIDDEN)

        users_to_share = request.data.get('users', [])
        
        shared_notes = []
        for userId in users_to_share:
            try:
                user = User.objects.get(id=userId)
                shared_note, created = SharedNote.objects.get_or_create(note=note, user=user)
                shared_notes.append(shared_note)
            except User.DoesNotExist:
                return Response({'error': f'User with username {userId} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SharedNoteSerializer(shared_notes, many=True)
        return Response({'message': 'Note shared successfully', 'shared_notes': serializer.data}, status=status.HTTP_201_CREATED)