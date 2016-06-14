from django.conf.urls import url, include, patterns
from rest_framework import routers

from items import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = patterns('',
   url(r'^', include(router.urls)),
)