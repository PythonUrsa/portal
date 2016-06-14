from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from chat.models import Message
from user_auth.serializers import PublicProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = PublicProfileSerializer()
    receipt = PublicProfileSerializer()

    class Meta:
        model = Message
        exclude = []


class MessageContactSerializer(PublicProfileSerializer):
    last_message = serializers.SerializerMethodField('get_last_msg')
    last_received_at = serializers.SerializerMethodField('get_last_msg_received_at')
    owner_id = serializers.IntegerField(source='id')

    class Meta:
        model = User
        fields = ('email', 'full_name', 'age', 'college', 'picture', 'owner_id',
                  'social_links', 'descriptions', 'id', 'last_message', 'last_received_at', 'is_online')

    def get_last_msg(self, obj):
        try:
            last_message = Message.objects.filter(receipt=obj.id).order_by('-created_at')[0].body
        except:
            return None
        return last_message

    def get_last_msg_received_at(self, obj):
        try:
            last_received_at = Message.objects.filter(receipt=obj.id).order_by('-created_at')[0].created_at
        except:
            return None
        return last_received_at
