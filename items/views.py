import django_filters

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser

from items.models import Item, Category
from items import serializers


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


class ItemFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(name="owner__id", lookup_type='exact')
    min_age = django_filters.NumberFilter(name="owner__age", lookup_type='gte')
    max_age = django_filters.NumberFilter(name="owner__age", lookup_type='lte')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    gender = django_filters.CharFilter(name="owner__gender", lookup_type='exact')
    college = django_filters.CharFilter(name="owner__college", lookup_type='exact')
    categories = CustomFilterList(name="category", lookup_type='in')

    class Meta:
        model = Item
        fields = ['id', 'user_id', 'type', 'min_age', 'max_age', 'min_price', 'max_price', 'gender', 'categories']

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        data = data.copy()
        if hasattr(data, 'college') and data['college'] == '':
            data.pop('college', None)
        if hasattr(data, 'gender') and data['gender'] == '':
            data.pop('gender', None)
        return super(ItemFilter, self).__init__(data, queryset, prefix, strict)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    PAGINATE_BY_PARAM = 'page_size'
    filter_class = ItemFilter

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', None)
        search_text = self.request.GET.get('search_text', None)
        queryset = super(ItemViewSet, self).get_queryset()

        if search_text:
            queryset = queryset.filter(Q(owner__first_name__icontains=search_text)
                                       | Q(owner__last_name__icontains=search_text)
                                       | Q(name__icontains=search_text)
                                       | Q(description__icontains=search_text))

        if sort_by:
            queryset = queryset.order_by('-modified_at')
        return queryset


