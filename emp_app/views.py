from datetime import datetime
from django.utils import timezone
from pytz import timezone as pytz_timezone
import json
from django.shortcuts import redirect,render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from emp_app.forms import EmployeeForm
from .models import Employee, Role, Department
# Create your views here.
def home(request):
    fname = None
    if request.user.is_authenticated:
        # Assuming the user profile has a 'fname' attribute
        fname = request.user.first_name 
    return render(request,"index.html",{'fname': fname})

def signup(request):
    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        try:
            user = User.objects.get(username=username)
            messages.error(request,"Username Exists. Try another")
            return redirect('home')
        except User.DoesNotExist:
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request,"Success! Account Created")
            return redirect('signin')
    return render(request,"signup.html")
def signin(request):
    if request.method == "POST":
        username=request.POST['username']
        pass1=request.POST['pass1'] 
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found. Please sign in')
            return redirect('home')
        user=authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,"index.html", {'fname':fname})
        else:
            messages.error(request,"Incorrect password")
            return redirect('home')
    return render(request,"signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('home')
def list(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'list.html', context)
def add(request):
    dept = Department.objects.all()
    role = Role.objects.all()
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
    elif request.method == 'GET':
        return render(request, 'add.html', {'form': form, 'dept': dept, 'role': role})
    else:
        messages.error(request, "User Not Added!")
    return HttpResponse("Error: User Not Added!")  # Return an HttpResponse object here


def search(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        try:
            employee = Employee.objects.get(pk=employee_id)
            return render(request, 'details.html', {'employee': employee})
        except Employee.DoesNotExist:
            messages.error(request,"User Not Found!")
            return render(request, 'index.html', {'error_message':messages.error})
    else:
        return render(request, 'search.html')

def update(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST,request.FILES,instance=employee)
        if form.is_valid():
            current_datetime = timezone.now()
            ist_timezone = pytz_timezone('Asia/Kolkata')  # IST timezone
            current_datetime_ist = current_datetime.astimezone(ist_timezone)
            form.instance.last_updated = current_datetime_ist
            form.save()
            return redirect('list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'update.html', {'form': form, 'employee_id': employee_id})


def delete(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        employee.delete()
        messages.error(request,"User Deleted Successfully!")
        return render(request, 'index.html', {'error_message':messages.error})
    except Employee.DoesNotExist:
        messages.error(request,"User Not Found!")
        return render(request, 'index.html', {'error_message':messages.error})
    