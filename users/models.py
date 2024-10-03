from django.db import models

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    sec = models.CharField(max_length=6)
    date = models.DateField()
    teacher = models.CharField(max_length=100)
    request = models.IntegerField()
    seat = models.IntegerField()
    note = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.code}, {self.name}, {self.year}, {self.semester}, {self.sec}, {self.date}, {self.teacher}, {self.request} {self.seat}, {self.note}"
    
class Student(models.Model):
    SID = models.CharField(max_length=10, unique=True)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.SID}, {self.first}, {self.last}, {self.faculty}"