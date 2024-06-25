from rest_framework import serializers
from .models import Thread, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', '_input', '_output', 'created_at')
        read_only_fields = ('user', '_output', 'thread')

class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'user', 'messages', 'created_at')
