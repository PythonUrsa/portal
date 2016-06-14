from django.conf.urls import url, include, patterns
from rest_framework import routers

from chat import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'messages', views.MessageViewSet)
router.register(r'message_contacts', views.MessageContactViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^new_messages$', views.new_message_api),
)