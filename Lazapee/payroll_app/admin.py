from django.contrib import admin
from .models import Payslip, Employee

# Register your models here.
admin.site.register(Employee)
admin.site.register(Payslip)