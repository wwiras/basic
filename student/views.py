from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Student
from .forms import MessageForm, SearchForm, StudentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# from .forms import PostForm

@login_required(login_url='/accounts/login/')
def student_new(request):

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.createdby = request.user
            student.save()
            # return redirect('post_detail', pk=post.pk)
            messages.success(request, "Student record with ID: " + str(student.pk) + " has been created ! ")
            return redirect(reverse_lazy('student_detail',kwargs={'pk': student.pk }))
    else:
        form = StudentForm()
    
    return render(request, 'student/student_new.html', {'form': form})

@login_required(login_url='/accounts/login/')
def student_edit(request,pk):

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.createdby = request.user
            student.save()
            # return redirect('post_detail', pk=post.pk)
            messages.success(request, "Student record with ID: " + str(student.pk) + " has been updated! ")
            return redirect(reverse_lazy('student_detail',kwargs={'pk': student.pk }))
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'student/student_edit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def student_detail(request,pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student/student_detail.html', {'student': student})


def student_list(request):
    students = Student.objects.all().order_by('created_date')
    # students = Student.objects.filter(name='G')
    return render(request, 'student/student_list.html', {'students': students})

@login_required(login_url='/accounts/login/')
def student_remove(request,pk):

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        if request.POST.get("submit_yes", ""):
            icnum = student.icnum
            student.delete()
            messages.success(request, "Student record with ID: " + str(icnum) + " has been removed! ")
            return redirect(reverse_lazy('student_home'))

    return render(request, 'student/student_confirm_delete.html', {'student': student, 'pk':pk})

def home(request):

    if request.method == "POST" :
        
        select_buttons = request.POST.get("select_buttons", "")
        search = request.POST.get("search", "")
        page = 1
        
        if select_buttons == 'icnum':
            students = Student.objects.filter(icnum__startswith=search).order_by('created_date')
            # select_buttons = 'icnum'
        elif select_buttons == 'course':
            students = Student.objects.filter(course__startswith=search).order_by('created_date')
            # select_buttons = 'course'
        else:
            students = Student.objects.filter(name__startswith=search).order_by('created_date')
            # select_buttons = 'name'
        
        if students:
            messages.success(request, str(len(students)) + " record(s) was/were found for keyword = " + str(request.POST.get("search", "")))
            page = 1
        else:
            messages.error(request, "Sorry, No record was found for keyword = " + str(request.POST.get("search", "")))
    else:

        select_buttons = request.GET.get("select_buttons", "")
        search = request.GET.get("search", "")

        if search:
            if select_buttons == 'icnum':
                students = Student.objects.filter(icnum__startswith=search).order_by('created_date')
            elif select_buttons == 'course':
                students = Student.objects.filter(course__startswith=search).order_by('created_date')
            else:
                students = Student.objects.filter(name__startswith=search).order_by('created_date')
        else:
            students = Student.objects.all().order_by('created_date')

        page = request.GET.get('page', 1)

    paginator = Paginator(students, 10)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'student/home.html', {'form': SearchForm(), 'students': students, 
        'search':search, 'select_buttons': select_buttons })