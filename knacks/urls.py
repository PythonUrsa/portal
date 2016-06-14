from django.conf.urls import url, include, patterns
from rest_framework import routers

from knacks import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'knacks', views.KnackViewSet)
router.register(r'knack_ideas', views.KnackIdeaViewSet)

urlpatterns = patterns('',
   url(r'^', include(router.urls)),
)