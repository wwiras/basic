from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Student
from .forms import MessageForm, SearchForm, StudentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField

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

def home_json(request):
    students = Student.objects.all().order_by('created_date')
    # students = Student.objects.filter(name='G')
    return render(request, 'student/home_json.html', {'students': students})

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


# Student JSON list filtering
class student_list_json(BaseDatatableView):
    order_columns = ['icnum','name','course', 'pk','link']

    def get_initial_queryset(self):
        # icnum = self.request.GET.get(u'icnum', '')
        # return Student.objects.filter(icnum=icnum)
        return Student.objects.all().order_by('icnum')

    def filter_queryset(self, qs):

        # Getting advanced filtering indicators for dataTables 1.10.13
        search = self.request.GET.get(u'search[value]', "")
        iSortCol_0 = self.request.GET.get(u'order[0][column]', "") # Column number 0,1,2,3,4
        sSortDir_0 = self.request.GET.get(u'order[0][dir]', "") # asc, desc
        
        # Choose which column to sort
        if iSortCol_0 == '1':
          sortcol = 'name'
        elif iSortCol_0 == '2':
          sortcol = 'course'
        else:
          sortcol = 'icnum'


        # Choose which sorting direction : asc or desc
        if sSortDir_0 == 'asc':
          sortdir = ''
        else:
          sortdir = '-'

        # Filtering if search value is key-in
        if search:
          # Initial Q parameter value
          qs_params = None

          # Filtering Course category
          course_list = dict(Student.COURSE_CHOICES)
          # print access_list
          course_search = ''
          for key in course_list:
            # print key, access_list[key]
            if search in course_list[key]:
              course_search = str(key)
              q = Q(course__icontains=course_search)
              qs_params = qs_params | q if qs_params else q

          # Filtering other fields
          q = Q(name__icontains=search)|Q(icnum__icontains=search)
          qs_params = qs_params | q if qs_params else q
   
          # Completed Q queryset
          # print qs_params
          qs = qs.filter(qs_params)
          # print 'qs :' + str(qs)
          # print 'qs :'

        # print 'sortdir + sortcol : ' + sortdir + sortcol
        return qs.order_by(sortdir + sortcol)
        # return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        # json_data = {}
        json_data = []

        for item in qs:
            json_data.append([
                item.icnum,
                item.name,
                # item.course,
                item.get_course_display(),
                str(item.pk),
                reverse_lazy('student_detail',kwargs={'pk': str(item.pk)})
            ])
            # print(json_data)
        return json_data
