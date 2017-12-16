from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Student
# from .forms import PostForm

def student_list(request):
    students = Student.objects.all().order_by('created_date')
    return render(request, 'student/student_list.html', {'students': students})