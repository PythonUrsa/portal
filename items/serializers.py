from django.contrib.auth import get_user_model
User = get_user_model()

from sorl.thumbnail import get_thumbnail
from rest_framework import serializers

from items.models import Item, Category


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_name = serializers.ReadOnlyField(source='owner.full_name')
    owner_college = serializers.ReadOnlyField(source='owner.college')
    owner_age = serializers.ReadOnlyField(source='owner.age')
    owner_picture = serializers.SerializerMethodField('get_owner_url')
    owner_picture_medium = serializers.SerializerMethodField('get_owner_medium_url')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    thumb_photo = serializers.SerializerMethodField('get_thumbnail_url')

    class Meta:
        model = Item
        exclude = ['owner', 'video']

    def get_owner_url(self, obj):
        if obj.owner.picture:
            return get_thumbnail(obj.owner.picture, '35x35', crop='center').url
        else:
            return None

    def get_owner_medium_url(self, obj):
        if obj.owner.picture:
            return get_thumbnail(obj.owner.picture, '70x70', crop='center').url
        else:
            return None

    def get_thumbnail_url(self, obj):
        if obj.photo:
            return get_thumbnail(obj.photo, '400x220', crop='center').url
        else:
            return None

    def is_valid(self, raise_exception=False):
        photo = self.initial_data.pop('photo')[0]
        if not isinstance(photo, str):
            self.initial_data.update({'photo': photo})
        # video = self.initial_data.pop('video')[0]
        # if not isinstance(video, str):
        #     self.instance.video = video
        return super(ItemSerializer, self).is_valid(raise_exception)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
