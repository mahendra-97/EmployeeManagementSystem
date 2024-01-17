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
from django.template.loader import render_to_string
import re

def employee_list(request):
    # employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html')

def employee_add(request):
    return render(request, 'employees/employee_add.html')

def employee_edit(request, id):
    print(id)
    employees = Employee.objects.get(id=id)
    employee = {
                    'id' : employees.id,
                    'name': employees.ename,
                    'phone': employees.ephone,
                    'email': employees.eemail,
                    'department': employees.edepartment,
                }
    print(employee)
    
    return JsonResponse({'employee': employee})

def employee_delete(request, id):
    # Retrieve the employee object or return a 404 error if not found
    employee = get_object_or_404(Employee, eid=id)

    if request.method == 'POST':
        # If the request is a POST request, delete the employee and redirect to the employee list view
        employee.delete()
        return redirect('employee-list-view')
    
    # If the request is not a POST request, render the confirmation page
    return render(request, 'employees/employee_delete.html', {'employee': employee})



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
        print("Hello world")
        try:
            # ename = request.POST.get('ename')
            # ephone = request.POST.get('ephone')
            # eemail = request.POST.get('eemail')
            # edepartment = request.POST.get('edepartment')

            data = json.loads(request.body.decode('utf-8'))
            ename = data.get('ename')
            ephone = data.get('ephone')
            eemail = data.get('eemail')
            edepartment = data.get('edepartment')

            # print(f"data = {ename},{ephone},{eemail},{edepartment}")
            
            # eemail_list = [email.strip() for email in eemail.split(',')]
            # for email in eemail_list:
            #     validate_email(email)

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
            print(request)
            data = json.loads(request.body.decode('utf-8'))
            ename = data.get('ename')
            ephone = data.get('ephone')
            eemail = data.get('eemail')
            edepartment = data.get('edepartment')

            # print(f"data = {ename},{ephone},{eemail},{edepartment}")
            
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
            employee = Employee.objects.get(eid=id)
            employee.delete()

            return JsonResponse({'success': 'Employee deleted successfully'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

