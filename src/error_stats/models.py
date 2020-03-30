from django.db import models
from students.models import Student
from django.urls import reverse

# Create your models here.

class Error_Stat(models.Model):
    num_tried = models.IntegerField()
    num_success = models.IntegerField()
    last_ran = models.DateTimeField(blank=True)
    last_failed = models.DateTimeField(blank=True)
    reliability = models.DecimalField(decimal_places=2, max_digits = 3)
    student_id = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("stat:stat-detail", kwargs={"id":self.id})
