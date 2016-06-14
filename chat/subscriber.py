import json

from django.contrib.auth import get_user_model
User = get_user_model()

from ws4redis.subscriber import RedisSubscriber

from chat.models import Message


class ChatSubscriber(RedisSubscriber):

    def publish_message(self, message, expire=None):
        msg = json.loads(message)
        try:
            Message.objects.create(sender=User.objects.get(pk=int(msg['sender_data']['user_id'])),
                                   receipt=User.objects.get(pk=int(msg['receipt_data']['owner_id'])),
                                   body=msg['message'])
        except:
            pass
        super(ChatSubscriber, self).publish_message(message, expire)