import requests

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers
from . import filters

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'movies': reverse('movies-list', request=request, format=format),
        'comments': reverse('comments-list', request=request, format=format),
        'top': reverse('movies-top-list', request=request, format=format)
    })

class MovieListCreate(generics.ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    filter_backends = (DjangoFilterBackend,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
                
        serializer.instance = models.Movie.objects.filter(
            title__iexact=serializer.validated_data['title']).first()
        
        if serializer.instance:            
            resp_status = status.HTTP_200_OK
            
        else:   
            try:
                remote_data = requests.get(
                    settings.OMDB['url'], {'apikey': settings.OMDB['apikey'],                        
                        't': serializer.validated_data['title']}
                ).json()
                
                if not eval(remote_data.get('Response', 'True')):
                    return Response(remote_data, status=status.HTTP_204_NO_CONTENT)
                    
            except Exception as e:                
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
            serializer.validated_data['data'] = remote_data
            self.perform_create(serializer)
            resp_status = status.HTTP_201_CREATED
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=resp_status, headers=headers)
        
class CommentListCreate(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all().order_by('-date_created')
    serializer_class = serializers.CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('movie',)
    
    def perform_create(self, serializer):
        serializer.save(movie=serializer.validated_data['movie'])
                  
class MovieTopList(generics.ListAPIView):
    
    queryset = models.Movie.objects.all()
    serializer_class = serializers.TopSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.TopMovieFilter