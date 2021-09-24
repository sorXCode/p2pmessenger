from datetime import datetime

from django.contrib.postgres.fields.array import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from uuid import uuid4

class MessageEntry(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now)

    def to_representation(self):
        return {
            'message_id': self.message_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content,
            'is_read': self.is_read,
            'timestamp': self.timestamp,
        }

    def save(self, *args, **kwargs):
        # Write message to messages history
        MessageHistory.objects.save_message(self.to_representation())


class MessageHistoryManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    def get_conversation_id(self, user_a, user_b):
        # return unique conversation id for two users
        conversation_id = "<->".join([str(user_id)
                                     for user_id in sorted([user_a.id, user_b.id, ])])

        return md5(conversation_id.encode()).hexdigest()

    def save_message(self, message):
        sender = message['sender']
        receiver = message['receiver']

        conversation_id = self.get_conversation_id(sender, receiver)
        message_history = self.get_or_none(conversation_id=conversation_id)

        # reconstruct message to a valid JSON
        message['sender'] = sender.id
        message['receiver'] = receiver.id
        message['message_id'] = uuid4()

        if not message_history:
            message_history = self.create(conversation_id=conversation_id,
                                          user_a=sender,
                                          user_b=receiver,
                                          messages=[message, ])
        else:

            message_history.messages.append(message)
            message_history.save()
        return message


class MessageHistory(models.Model):
    conversation_id = models.CharField(
        max_length=255, db_index=True, primary_key=True)
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True, related_name='user_a')
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True, related_name='user_b')
    messages = models.JSONField(encoder=DjangoJSONEncoder)
    added_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = MessageHistoryManager()

    class Meta:
        ordering = ('-updated_at',)

    def receiver_mark_as_read(self, receiver):
        for message in self.messages[::-1]:
            # only receiver can mark his/her message as read
            if message["receiver"]==receiver:
                if message["is_read"]==False:
                    message["is_read"] = True
                else:
                    # break on most recent "read" message by user
                    break
        self.save()
    
