
import json
from django.core.exceptions import ValidationError

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from djangochannelsrestframework import permissions as dcrf_permissions
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import \
    ObserverModelInstanceMixin
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .models import MessageHistory
from .serializers import (LastMessagesSerializer, MessageEntrySerializer,
                         MessageHistorySerializer)


class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    permission_classes = [dcrf_permissions.IsAuthenticated, ]
    queryset = MessageHistory.objects.all()
    lookup_field = "pk"
    mapped_field = "conversation_id"

    def get_queryset(self, *args, **kwargs):
        current_user = self.scope['user']

        if kwargs.get('action') in ['subscribe_instance', 'retrieve', 'update']:
            pk_field = {self.mapped_field: f'{kwargs.get(self.lookup_field)}'}
            return self.get_serializer_class(*args, **kwargs).Meta.model.objects.filter(Q(**pk_field) & (Q(user_a=current_user) | Q(user_b=current_user))).all()

    def get_serializer_class(self, *args, **kwargs):
        action = kwargs.get('action')
        if action in ['subscribe_instance', 'retrieve']:
            return MessageHistorySerializer
        elif action == "update":
            return LastMessagesSerializer
        elif action == "chat":
            return MessageEntrySerializer  # action=chat
        raise ValidationError(f"no serializer class specified for '{action}'")

    def get_object(self, **kwargs):
        queryset = self.filter_queryset(
            queryset=self.get_queryset(**kwargs), **kwargs)

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.mapped_field: kwargs[lookup_url_kwarg]}

        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj

    @classmethod
    def _encode_json(cls, content):
        return json.dumps(content, cls=DjangoJSONEncoder)
    
    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content, cls=DjangoJSONEncoder)


    @action()
    def chat(self, data, *args, **kwargs):
        """
            Using standard create logics from the CreateModelMixin
        """
        serializer = self.get_serializer(data=data, action_kwargs=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self._encode_json(serializer.data), status.HTTP_201_CREATED

    @action()
    def mark_as_read(self, data, *args, **kwargs):
        pass