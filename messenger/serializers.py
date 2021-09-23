from rest_framework import serializers
from .models import MessageEntry, MessageHistory

class MessageEntrySerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field='id')
    is_read = serializers.BooleanField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    message_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = MessageEntry
        fields = ('message_id', 'sender','receiver','content','is_read','timestamp')
    

    def create(self, validated_data):
        validated_data['sender'] =  self.context['scope']['user']
        return super().create(validated_data)


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ('conversation_id', 'user_a', 'user_b', 'messages')

class LastMessagesSerializer(MessageHistorySerializer):
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = MessageHistory
        fields = ('conversation_id', 'user_a', 'user_b', 'last_message')
    
    def get_last_message(self, obj):
        return obj.messages[-1]


class MarkAsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ('conversation_id', 'message_id')

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data['conversation_id']:
            pass