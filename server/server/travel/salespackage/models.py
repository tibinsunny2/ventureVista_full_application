from django.db import models

class Trip(models.Model):
    title = models.CharField(max_length=255)
    amount = models.IntegerField()
    duration = models.IntegerField()
    location = models.CharField(max_length=255)
    rating = models.IntegerField()
    username = models.CharField(max_length=255)
    no_of_peoples=models.CharField(max_length=255)
    def __str__(self):
        return self.title