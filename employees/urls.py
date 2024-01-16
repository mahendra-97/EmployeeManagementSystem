from django.urls import path
from .views import EmployeeAPI, employee_list, employee_add, employee_edit,employee_delete

urlpatterns = [
    path('api/employees/', EmployeeAPI.as_view(), name='employee-api'),
    path('api/employees/<int:id>/', EmployeeAPI.as_view(), name='employee-detail-api'),
    # path('', employee_list, name='employee-list-view'),
    # path('employee-add/', employee_add, name='employee-add-view'),
    # path('employee-edit/', employee_edit, name='employee-edit-view'),


    # HTML views
    path('employees', employee_list, name='employee-list-view'),
    path('employees/add/', employee_add, name='employee-add-view'),
    path('employees/edit/<int:id>/', employee_edit, name='employee-edit-view'),
    path('employees/delete/<int:id>/', employee_delete, name='employee-delete-view'),
    
]