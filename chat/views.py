from itertools import chain

from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from chat import serializers
from chat.models import Message


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.none()
    serializer_class = serializers.MessageSerializer
    paginate_by = 100

    def get_queryset(self):
        try:
            companion = self.request.GET['companion']
        except:
            return None
        queryset = Message.objects.filter(
            (Q(sender=self.request.user.id) & Q(receipt=int(companion))) |
            (Q(receipt=self.request.user.id) & Q(sender=int(companion))))
        for msg in queryset:
            msg.is_read = True
            msg.save()
        return queryset


class MessageContactViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = serializers.MessageContactSerializer
    paginate_by = 100

    def get_queryset(self):
        receipt_of = Message.objects.filter(receipt=self.request.user.id)\
            .values_list('sender', flat=True).distinct()

        sender_of = Message.objects.filter(sender=self.request.user.id)\
            .values_list('receipt', flat=True).distinct()

        contact_ids = list(chain(receipt_of, sender_of))

        queryset = User.objects.filter(id__in=contact_ids)
        return queryset


class NewMessagesAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        unread_messages = Message.objects.filter(Q(receipt=request.user) & Q(is_read=False))
        serializer = serializers.MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)

new_message_api = NewMessagesAPIView.as_view()