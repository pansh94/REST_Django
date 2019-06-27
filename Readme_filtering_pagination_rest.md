# Filter backend with URL query parameter 
The django-filter library includes a DjangoFilterBackend class which supports highly customizable field filtering for REST
framework. Add django_filters in installed app in settings.py and write the below code and hit the url.
If all you need is simple equality-based filtering, you can set a filterset_fields attribute on the view, or viewset, listing
the set of fields you wish to filter against.
```
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    
    
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ('name',) # enable filter with specific fields
    search_fields = ('name', 'description')
    pagination_class = ProductPagination

# use to filter query set
    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__lte=now,
            )
        return queryset
```

## Enable full text search in REST(SEARCH_FILTER)
The SearchFilter class supports simple single query parameter based searching, and is based on the Django admin's search
functionality.The SearchFilter class will only be applied if the view has a search_fields attribute set. The search_fields
attribute should be a list of names of text type fields on the model, such as CharField or TextField.
You can also perform a related lookup on a ForeignKey or ManyToManyField with the lookup API double-underscore notation:
```
search_fields = ('username', 'email', 'profile__profession')
```
By default, searches will use case-insensitive partial matches. The search parameter may contain multiple search terms, which
should be whitespace and/or comma separated. If multiple search terms are used then objects will be returned in the list only
if all the provided terms are matched.
1. '^' Starts-with search.
2. '=' Exact matches.
3. '@' Full-text search. (Currently only supported Django's MySQL backend.)
4. '$' Regex search.
```
search_fields = ('=username', '=email')
```
it's possible to subclass the SearchFilter and override the get_search_fields() function.

# Pagination
REST framework includes support for customizable pagination styles. This allows you to modify how large result sets are split
into individual pages of data.
You can also set the pagination class on an individual view by using the pagination_class attribute or globaly in settings.py.



