from django.db import models

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=5)
    subject_name = models.CharField(max_length=64)
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=1)
    seat = models.CharField(max_length=4)
    status = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.code}, {self.subject_name}, {self.year}, {self.semester}, {self.seat}, {self.status}"
    
class Student(models.Model):
    student_code = models.CharField(max_length=10, unique=True)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.student_code} {self.first} {self.last}"