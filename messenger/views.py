from django.db.models import Q
from rest_framework import permissions, viewsets

from .serializers import LastMessagesSerializer, MessageHistorySerializer


class MessageHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        action = self.action
        current_user = self.request.user

        if action == 'list':
            # list request returns objects where the logged in user is either user_a or user_b
            return self.get_serializer_class().Meta.model.objects.filter(Q(user_a=current_user) | Q(user_b=current_user)).all()
        elif action == 'retrieve':
            pk_field = {"pk": self.kwargs[self.lookup_field]}
            return self.get_serializer_class().Meta.model.objects.filter(Q(**pk_field) & (Q(user_a=current_user) | Q(user_b=current_user))).all()

    def get_serializer_class(self):
        serializer_classes = {
            'list': LastMessagesSerializer,
            'retrieve': MessageHistorySerializer
        }
        return serializer_classes[self.action]
