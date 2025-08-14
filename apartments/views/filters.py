import django_filters
from apartments.models import Apartment, Category




class ApartmentFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    city = django_filters.CharFilter(field_name="address__city", lookup_expr='icontains')

    rooms_min = django_filters.NumberFilter(field_name="rooms", lookup_expr='gte')
    rooms_max = django_filters.NumberFilter(field_name="rooms", lookup_expr='lte')

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category"
    )

    class Meta:
        model = Apartment
        fields = ['price_min', 'price_max', 'city', 'rooms_min', 'rooms_max', 'category']
