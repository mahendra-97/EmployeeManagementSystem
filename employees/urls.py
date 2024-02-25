from django.urls import path
from . import views
# , EmployeeAPI, home, login, employee_list, employee_add, employee_edit

urlpatterns = [
    # API Views
    path('api/signup/', views.signup_api, name='signup-api'),
    path('api/login/', views.login_api, name='login-api'),
    path('api/employees/', views.EmployeeAPI.as_view(), name='employee-api'),
    path('api/employees/<int:id>/', views.EmployeeAPI.as_view(), name='employee-detail-api'),

    # HTML views
    path('home', views.home, name='Home'),
    path('signup_form', views.signup, name='Signup'),
    path('login_form', views.login, name='Login'),
    path('employees', views.employee_list, name='employee-list-view'),
    path('employees/add/', views.employee_add, name='employee-add-view'),
    path('employees/edit/<int:id>/', views.employee_edit, name='employee-edit-view'),
]