from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    person_id = models.IntegerField()
    arrival_time = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return f"{self.person_id} - {self.arrival_time}"


class Student_record(models.Model):
    person_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    program_of_study = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=100)
