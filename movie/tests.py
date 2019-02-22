from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase
from .models import Movie, Comment

class MovieTests(APITestCase):
    fixtures = ['movie']
        
    def test_fixture(self):
        self.assertEqual(Movie.objects.count(), 6)
        self.assertEqual(Comment.objects.count(), 36)
        
    def test_movies(self):
    
        url = reverse('movies-list') 
        
        #Test creation
        data = {'title': 'Titanic'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 7)
        self.assertEqual(Movie.objects.get(id=7).data['Title'], 'Titanic')
            
        #Test non duplicating
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), 7)
        self.assertEqual(Movie.objects.get(id=7).data['Title'], 'Titanic')
            
        #Test listing
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 7)
        
    def test_comments(self):
        
        url = reverse('comments-list')
        
        #test creation
        data = {'body': 'comment', 'movie': '1'}
        response = self.client.post(url, data, format='json')        
        self.assertEqual(response.data['movie'], 1)                
        self.assertEqual(Comment.objects.count(), 37)
        
        #Test listing
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 37)

    def test_top(self):
                
        url = reverse('movies-top-list')
        
        #test rank with no date given (all equal)
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 6)
        for movie in response.data:
            self.assertEqual(movie['rank'], 1)
            self.assertEqual(movie['total_comments'], 6)
        
        #test date filters
        data = {'date_range_after': '2019-02-15', 'date_range_before': '2019-02-19'}    
        expected_seq = [(1,4),(2,3),(2,3),(2,3),(3,2),(3,2)]        
        response = self.client.get(url, data, format='json')
        for movie, v in zip(response.data, expected_seq):
            self.assertEqual(movie['rank'], v[0])
            self.assertEqual(movie['total_comments'], v[1])
            
        data = {'date_range_before': '2019-02-15'}    
        expected_seq = [(1,5),(2,3),(2,3),(3,2),(3,2),(4,0)]        
        response = self.client.get(url, data, format='json')
        for movie, v in zip(response.data, expected_seq):
            self.assertEqual(movie['rank'], v[0])
            self.assertEqual(movie['total_comments'], v[1])
                        
        data = {'date_range_after': '2019-02-19'}    
        expected_seq = [(1,3),(1,3),(2,1),(2,1),(2,1),(2,1)]        
        response = self.client.get(url, data, format='json')
        for movie, v in zip(response.data, expected_seq):
            self.assertEqual(movie['rank'], v[0])
            self.assertEqual(movie['total_comments'], v[1])
            
            
            