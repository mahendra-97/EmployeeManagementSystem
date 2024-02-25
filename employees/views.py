import json
from django.urls import path
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee, User
from .forms import UserForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
import re

def home(request):
    return render(request, 'employees/home.html')

def employee_list(request):
    return render(request, 'employees/employee_list.html')

def employee_add(request):
    return render(request, 'employees/employee_add.html')

def employee_edit(request, id):
    employees = Employee.objects.get(id=id)
    employee = {
                    'id' : employees.id,
                    'name': employees.ename,
                    'phone': employees.ephone,
                    'email': employees.eemail,
                    'department': employees.edepartment,
                }
    return JsonResponse({'employee': employee})

def signup(request):
    return render(request, 'employees/signup.html')

def login(request):
    print("In Login View")
    return render(request, 'employees/login.html')

def signup_api(request):
    print("in signup api")
    if request.method == 'POST':
        form = UserForm(request.POST)
        # print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            contactno = form.cleaned_data['contactno']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            user = User.objects.create(username=username, name=name, contactno=contactno, email=email, password=hashed_password)
            # print(username, name, contactno,email,password,hashed_password)
            return JsonResponse({'status_code': 200, 'success': 'Signup successful'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = UserForm()
    return JsonResponse({'form': form})

def login_api(request):
    print("In Loginsubmit View")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # Retrieve the user from your custom database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            # Authentication failed
            return JsonResponse({'success': False, 'message': 'Invalid username or password'}, status=400)

    else:
        # Handle invalid request method
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

class EmployeeAPI(APIView):

    def get(self, request, id=None):
        try:
            if id:
                employee = Employee.objects.get(id=id)
                data = {
                    'id': employee.id,
                    'name': employee.ename,
                    'phone': employee.ephone,
                    'email': employee.eemail,
                    'department': employee.edepartment,
                }
            else:
                employees = Employee.objects.all()
                data = [{'id': emp.id, 'name': emp.ename, 'phone': emp.ephone, 'email': emp.eemail, 'department': emp.edepartment} for emp in employees]

            return JsonResponse({'data': data})

        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        try:

            data = json.loads(request.body.decode('utf-8'))
            print(data)
            ename = data.get('ename')
            ephone = data.get('ephone')
            eemail = data.get('eemail')
            edepartment = data.get('edepartment')

            pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
            if not re.match(pattern, ephone):
                return JsonResponse({'error': 'Invalid phone number'}, status=400)

            employee = Employee.objects.create(ename=ename, ephone=ephone, eemail=eemail, edepartment=edepartment)

            return JsonResponse({'id': employee.id, 'success': 'Employee created successfully'})

        except ValidationError as e:
            data = {'status':'error','error_code': 422, 'message': "['Enter a valid email address.']".format(e)}
            return JsonResponse(data, status=422)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, id=None):
        try:
            data = json.loads(request.body.decode('utf-8'))
            ename = data.get('ename')
            ephone = data.get('ephone')
            eemail = data.get('eemail')
            edepartment = data.get('edepartment')
            
            employee = Employee.objects.get(id=id)
            employee.ename = ename
            employee.ephone = ephone
            employee.eemail = eemail
            employee.edepartment = edepartment
            employee.save()

            return JsonResponse({'success': 'Employee updated successfully'})

        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

        except ValidationError as e:
            data = {'status':'error','error_code': 422, 'message': "['Enter a valid email address.']".format(e)}
            return JsonResponse(data, status=422)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()

            return JsonResponse({'success': 'Employee deleted successfully'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

