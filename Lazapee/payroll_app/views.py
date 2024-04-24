from django.shortcuts import render

def employees(request):
    return render(request, 'payroll_app/employees.html')