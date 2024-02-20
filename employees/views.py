import json
from django.urls import path
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
import re

def home(request):
    return render(request, 'employees/home.html')

def employee_list(request):
    # employees = Employee.objects.all()
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

def login_employeer(request):
    print("In Login View")
    return render(request, 'employees/login.html')

def login_view(request):
    print("In Loginsubmit View")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employees') 
        else:
            # Return an error message indicating invalid credentials
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        # Render the login page template
        return render(request, 'login.html')

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

