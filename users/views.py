from django.shortcuts import render,redirect, get_object_or_404
from .models import Subject, Student
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@csrf_exempt
def login_toweb(request):
    if request.user.is_authenticated :
        user = request.user
        
        return render(request, "quota_request.html")
        
    elif request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect("/admin")
            subjects = Subject.objects.all()
            student = Student.objects.get(SID=request.user)
            return render(request, "quota_request.html", {"subjects": subjects, "student": student})
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, "login.html")
    return render(request, "login.html")
            
def logout_formweb(request):
    logout(request)
    return redirect("/")

def quota_request(request):
    if request.user.is_authenticated:
        subjects = Subject.objects.all()
        student = Student.objects.get(SID=request.user)
        return render(request, "quota_request.html", {"subjects": subjects, "student": student})
    else:
        messages.error(request, "You need to log in to access this page.")
        return redirect("/")

def quota_result(request):
    student = get_object_or_404(Student, SID=request.user)
    registered_subjects = Subject.objects.filter(code__in=student.my_subject)
    return render(request, "quota_result.html", {"registered_subjects": registered_subjects, "student": student})


def registration(request):
    if request.method == "POST":
        Student_ID = request.POST["Student ID"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password != password2:
            messages.error(request, "Password must be the same one!")
            return redirect("/register")
        
        elif User.objects.filter(username=Student_ID):
            messages.error(request, "This Student ID is already used!! ")
            return redirect("/register")
        
        else:    
            User_Pass = User.objects.create_user(
                username = Student_ID,
                password = password
            )
            User_Pass.save()
             
            Naksuksa =Student(SID = User_Pass,
                              first = name,
                              last = surname)
            Naksuksa.save()
            messages.success(request, "registered successfully")
            return redirect("/")
    else:
        return render(request, "register.html")
    
def register_subject(request, subject_id):
    subject = get_object_or_404(Subject, id= subject_id)
    student = get_object_or_404(Student, SID=request.user)
    
    if subject.seat > subject.request:
        subject.request += 1
        subject.save()
        
        student.add_to_list(subject.code)
        subject.add_to_list(f"{student.SID} {student.first} {student.last}")
        messages.success(request, "Enroll successfully")
    else:
        messages.error(request, "No seats available")
    
    return redirect("/request")

def cancel_registration(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    student = get_object_or_404(Student, SID=request.user)

    if subject.code in student.my_subject:
        student.remove_form_list(subject.code)
        subject.remove_form_list(f"{student.SID} {student.first} {student.last}")
        subject.request -= 1
        subject.save()
        messages.success(request, "Drop successfully.")
    else:
        messages.error(request, "You are not registered for this course.")

    return redirect('/result')
