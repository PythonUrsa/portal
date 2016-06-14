from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from knacks.models import Knack, KnackIdea, Category


class KnackSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    owner_name = serializers.ReadOnlyField(source='owner.full_name')
    owner_college = serializers.ReadOnlyField(source='owner.college')
    owner_age = serializers.ReadOnlyField(source='owner.age')
    owner_online = serializers.ReadOnlyField(source='owner.is_online')
    owner_picture = serializers.SerializerMethodField('get_owner_url')
    owner_picture_medium = serializers.SerializerMethodField('get_owner_medium_url')
    thumb_photo = serializers.SerializerMethodField('get_thumbnail_url')

    class Meta:
        model = Knack
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
        return super(KnackSerializer, self).is_valid(raise_exception)


class KnackIdeaSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    thumb_photo = serializers.SerializerMethodField('get_photos')

    class Meta:
        model = KnackIdea

    def get_photos(self, obj):
        arr = []
        photos = obj.knackideaimage_set.all()
        for item in photos:
            arr.append(get_thumbnail(item.photo, '219x147', crop='center').url)
        return arr


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
