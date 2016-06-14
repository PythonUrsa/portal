import django_filters

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from social.apps.django_app.default.models import Code

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from social.backends.facebook import FacebookOAuth2

from knacks.models import Knack, KnackIdea, Category
from knacks import serializers

SOCIAL_BACKENDS = {
    FacebookOAuth2.name: FacebookOAuth2
}


def fb_login(request):
    context = RequestContext(request, {'user': request.user})
    backend_name = 'facebook'
    backend_class = SOCIAL_BACKENDS.get(backend_name)
    request.user.backend = '{0}.{1}'.format(backend_class.__module__, backend_class.__name__)
    if request.user is not None:
        if request.user.is_active:
            login(request, request.user)

    response = HttpResponseRedirect("/#/welcome-profile")
    if backend_name:
        code = Code.make_code(request.user.email)
        response.set_cookie('social_code', code.code)
        response.set_cookie('social_backend', backend_name)
    return response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    paginate_by = 100


class CustomFilterList(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            values = [v for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.name, self.lookup_type): values})
        return qs


class KnackFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner_id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college", lookup_type='iexact')
    categories = CustomFilterList(name="category", lookup_type='in')

    class Meta:
        model = Knack
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'categories']
        # fields = {'id', 'type', 'min_price', 'max_price', 'gender' }

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        return super(KnackFilter, self).__init__(data, queryset, prefix, strict)


class KnackViewSet(viewsets.ModelViewSet):
    queryset = Knack.objects.all()
    serializer_class = serializers.KnackSerializer
    PAGINATE_BY_PARAM = 'page_size'
    filter_class = KnackFilter

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search_text = self.request.GET.get('search_text', None)
        queryset = super(KnackViewSet, self).get_queryset()

        if search_text:
            queryset = queryset.filter(Q(owner__first_name__icontains=search_text)
                                       | Q(owner__last_name__icontains=search_text)
                                       | Q(name__icontains=search_text)
                                       | Q(description__icontains=search_text))

        if sort_by:
            queryset = queryset.order_by('-modified_at')
        return queryset


class KnackIdeaFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner_id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college", lookup_type='iexact')
    categories = CustomFilterList(name="category", lookup_type='in')

    class Meta:
        model = Knack
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'categories']
        # fields = {'id', 'type', 'min_price', 'max_price', 'gender' }

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        return super(KnackIdeaFilter, self).__init__(data, queryset, prefix, strict)


class KnackIdeaViewSet(viewsets.ModelViewSet):
    queryset = KnackIdea.objects.all()
    serializer_class = serializers.KnackIdeaSerializer
    PAGINATE_BY_PARAM = 'page_size'
    # filter_class = KnackIdeaFilter
    # filter_class = KnackIdeaFilter

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super(KnackIdeaViewSet, self).get_queryset()
        queryset = queryset.order_by('-modified_at')
        return queryset