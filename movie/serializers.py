import requests

from . import models
from rest_framework import serializers 

class MovieSerializer(serializers.ModelSerializer):
    data =  serializers.JSONField(read_only=True)    
    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'data')                      
        
class CommentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Comment
        fields = ('body', 'movie', 'date_created')
        
class TopSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()   
    rank = serializers.IntegerField()
    class Meta:
        model = models.Movie
        fields = ('id', 'total_comments', 'rank')
        
