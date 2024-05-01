from django.shortcuts import render

def employees(request):
    return render(request, 'payroll_app/employees.html')

def create_employee(request):
    return render(request, 'payroll_app/create_employee.html')

def payslips(request):
    return render(request, 'payroll_app/payslips.html')

def update_employee(request):
    return render(request, 'payroll_app/update_employee.html')

def view_payslip(request):
    return render(request, 'payroll_app/view_payslip.html')