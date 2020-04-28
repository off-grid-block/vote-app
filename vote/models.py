from django.db import models


class Poll(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100)
