from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        UNAVAILABLE = 'Unavailable', 'Unavailable'
    
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=1)
    year = models.CharField(max_length=4)
    request = models.IntegerField(default=0)
    seat = models.IntegerField()
    note = models.CharField(max_length=100, default="-")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    my_student = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.code}, {self.name}, {self.semester},  {self.year}, {self.request}, {self.seat}, {self.note}, {self.status}"
        
    def add_to_list(self,item):
        self.my_student.append(item)
        self.save()
        
    def remove_form_list(self, item):
        if item in self.my_student:
            self.my_student.remove(item)
            self.save()
        
    
class Student(models.Model):
    SID = models.OneToOneField(User, on_delete=models.CASCADE)
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    my_subject = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.SID}, {self.first}, {self.last}, {self.my_subject}"
    
    def add_to_list(self,item):
        self.my_subject.append(item)
        self.save()
        
    def remove_form_list(self, item):
        if item in self.my_subject:
            self.my_subject.remove(item)
            self.save()
    