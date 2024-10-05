from django.contrib import admin
from .models import Subject, Student

# Register your models here.
class Subject_Add(admin.ModelAdmin):
    model = Subject
    exclude = ['request']
    list_display = ['code', 'name', 'semester', 'year', 'seat', 'note', 'status']
    
class Student_Display(admin.ModelAdmin):
    model = Student
    list_display = ['SID', 'first', 'last', 'my_subject']

admin.site.register(Subject, Subject_Add)
admin.site.register(Student, Student_Display)