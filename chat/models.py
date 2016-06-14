from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(User, null=False, blank=False, related_name='senders')
    receipt = models.ForeignKey(User, null=False, blank=False, related_name='receipts')
    body = models.TextField(null=False, blank=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.sender.get_full_name()