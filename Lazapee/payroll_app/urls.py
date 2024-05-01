from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name='employees'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('payslips/', views.payslips, name='payslips'),
    path('update_employee/', views.update_employee, name='update_employee'),
    path('view_payslip/', views.view_payslip, name='view_payslip'),
]