from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

ITEM_TYPES = (
    ('O', 'Offered'),
    ('W', 'Wanted'),
)


class Item(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False)
    price = models.IntegerField(default=0, blank=False)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, null=False, blank=False)
    photo = models.ImageField(upload_to='items/images/', null=True, blank=True)
    video = models.ImageField(upload_to='items/videos/', null=True, blank=True)

    owner = models.ForeignKey(User, null=False, blank=False, related_name='items')

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return u'%s\'s %s' % (self.owner, self.name)

    def __unicode__(self):
        return u'%s\'s %s' % (self.owner, self.name)


class Category(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'