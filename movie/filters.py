import django_filters 
from django.db.models import Count, Q, Window, functions, F
class TopMovieFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(
        field_name='comments__date_created', method='anno_dates')
    
    def anno_dates(self, queryset, name, value):    
        if value:
            if value.start is not None and value.stop is not None:
                lookup_expr = 'range'
                value = (value.start, value.stop)                
            elif value.start is not None:
                lookup_expr = 'gte'
                value = value.start
            elif value.stop is not None:
                lookup_expr = 'lte'
                value = value.stop               
                        
            dense_rank = Window(expression=functions.DenseRank(),
                order_by=F('total_comments').desc())
                
            queryset = queryset.annotate(total_comments=Count('comments', 
                filter=Q(**{'__'.join([name, lookup_expr]):value}))
                ).annotate(rank=dense_rank).order_by('-total_comments', 'id')
                
        return queryset
