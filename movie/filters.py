import django_filters 
from django import forms
from django.db.models import Count, Q, Window, functions, F

class MovieFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(('data__Year', 'Production year'),))
    
    genre = django_filters.CharFilter(field_name='data__Genre', 
        label='Genre', lookup_expr='icontains')

    actors = django_filters.CharFilter(field_name='data__Actors', 
        label='Actors', lookup_expr='icontains')
    
class TopMovieFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(
        field_name='comments__date_created', method='anno_dates')
        
    def filter_queryset(self, queryset):        
        
        if self.form.cleaned_data['date_range'] is None:            
            dense_rank = Window(
                expression=functions.DenseRank(),                
                order_by=F('total_comments').desc())        
            queryset = queryset.annotate(total_comments=Count('comments')
                ).annotate(rank=dense_rank).order_by('-total_comments', 'id')
                
        return super().filter_queryset(queryset)       
    
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

