from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteChange, SharedNote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class NoteChangeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = NoteChange
        fields = ['timestamp', 'user', 'changes']

class SharedNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SharedNote
        fields = '__all__'
        
class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Note
        fields = '__all__'


class NoteVersionSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    version_history = NoteChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = '__all__'