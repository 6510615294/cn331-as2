from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    year = models.IntegerField()
    request = models.IntegerField()
    seat = models.IntegerField()
    note = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code}, {self.name}, {self.semester}, {self.year}, {self.request}, {self.seat}, {self.note}"
    
class Student(models.Model):
    SID = models.OneToOneField(User, on_delete=models.CASCADE)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.SID}, {self.first}, {self.last}"