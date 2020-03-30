from django.db import models
from django.urls import reverse

# Create your models here.

class Student(models.Model):
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(blank = True, max_length=50)

    def get_absolute_url(self):
        return reverse("student:student-detail",kwargs={"my_id": self.id})
