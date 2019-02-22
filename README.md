# Movie Database API

This API collects data from http://www.omdbapi.com/, lets posting comments to each movie and shows ranking based on number of comments.

## Requirements

1. Postgresql
2. Dajngo > 2.0
3. django-filter
4. djangorestframework
5. requests==2.20.1

## Usage

1. Clone this repo using ``git clone`` to django project
2. Add ``movie`` to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ....
    'rest_framework',
    'django_filters',
    'movie'
]  
OMDB = {
    'url': 'http://www.omdbapi.com',
    'apikey': 'ENTER_API_KEY'
}  
```
3. Import the api urls to your projects ``urls.py`` file:

```python
urlpatterns = [
    path('', include('movie.urls')),
]
```
## Notes

You can use movie.json to load data used for tests.
