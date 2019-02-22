from django.db import models
from django.db import connection

#only postgres supports json natively
if connection.vendor == 'postgresql':
    from django.contrib.postgres.fields import JSONField
else:
    from jsonfield import JSONField
    
class Movie(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    data = JSONField()

    class Meta:
        unique_together = (('title', 'data'),)
        
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    