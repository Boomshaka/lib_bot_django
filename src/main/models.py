from django.db import models

# Create your models here.

class RoomBook(models.Model):
    target_time = models.IntegerField()
    target_room = models.IntegerField()