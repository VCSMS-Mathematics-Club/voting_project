from django.db import models

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Voter(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address
