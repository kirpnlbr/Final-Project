from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name='employees'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('payslips/', views.payslips, name='payslips'),
    path('create_payslip/', views.create_payslip, name='create_payslip'),
    path('update_employee/', views.update_employee, name='update_employee'),
    path('view_payslip/<int:payslip_id>/', views.view_payslip, name='view_payslip'),
    path('delete_payslip/<int:payslip_id>/', views.delete_payslip, name='delete_payslip'),
    path('update_employee/<str:id_number>/', views.update_employee, name='update_employee'),
    path('delete_employee/<str:id_number>/', views.delete_employee, name='delete_employee'),
    path('add_overtime/<str:id_number>/', views.add_overtime, name='add_overtime'),
]