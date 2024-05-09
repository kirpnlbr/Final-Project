from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip
from django.urls import reverse
from django.contrib import messages

def employees(request):
    employees_list = Employee.objects.all()
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        overtime_hours = float(request.POST.get('overtime_hours', 0))
        employee = get_object_or_404(Employee, id_number=employee_id)
        overtime_rate = (employee.rate / 160) * 1.5 * overtime_hours
        employee.overtime_pay = employee.getOvertime() + overtime_rate
        employee.save()
        return redirect('employees')
    context = {'employees': employees_list}
    return render(request, 'payroll_app/employees.html', context)

def create_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        
        try:
            rate = float(rate)
            allowance = float(allowance) if allowance else None
        except ValueError:
            messages.error(request, 'Invalid input for rate or allowance.')
            return render(request, 'payroll_app/create_employee.html')
        
        if Employee.objects.filter(id_number=id_number).exists():
            messages.error(request, 'Employee with this ID number already exists.')
            return render(request, 'payroll_app/create_employee.html')
        

        
        Employee.objects.create(
            name=name,
            id_number=id_number,
            rate=rate,
            allowance=allowance
        )
        return redirect('employees')
    
    return render(request, 'payroll_app/create_employee.html')

def update_employee(request, id_number):
    employee = Employee.objects.filter(id_number=id_number).first()
    
    if not employee:
        context = {'error': 'Employee not found.'}
        return render(request, 'payroll_app/update_employee.html', context)

    if request.method == 'POST':
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        
        try:
            rate = float(rate)
            allowance = float(allowance) if allowance else None
        except ValueError:
            context = {'error': 'Invalid input for rate or allowance.'}
            return render(request, 'payroll_app/update_employee.html', context)
        
        employee.name = name
        employee.rate = rate
        employee.allowance = allowance
        employee.save()
        
        return redirect('employees')
    
    context = {'employee': employee}
    return render(request, 'payroll_app/update_employee.html', context)

def delete_employee(request, id_number):
    employee = Employee.objects.filter(id_number=id_number).first()
    
    if not employee:
        context = {'error': 'Employee not found.'}
        return render(request, 'payroll_app/delete_employee.html', context)

    if request.method == 'POST':
        employee.delete()
        return redirect('employees')
    
    context = {'employee': employee}
    return render(request, 'payroll_app/delete_employee.html', context)

def add_overtime(request, id_number):
    employee = get_object_or_404(Employee, id_number=id_number)

    if request.method == 'POST':
        overtime_hours_input = request.POST.get('overtime_hours')

        if overtime_hours_input is None or overtime_hours_input.strip() == '':
            messages.error(request, 'Error: Overtime hours cannot be blank.')
            return redirect(reverse('employees'))

        try:
            overtime_hours = float(overtime_hours_input)
            overtime_pay = (employee.rate / 160) * 1.5 * overtime_hours

            if employee.overtime_pay is None:
                employee.overtime_pay = 0.0

            employee.overtime_pay += overtime_pay
            employee.save()

            messages.success(request, 'Overtime added successfully.')
        except ValueError:
            messages.error(request, 'Error: Please enter a valid number for overtime hours.')

        return redirect(reverse('employees'))

    context = {'employees': Employee.objects.all()}
    return render(request, 'payroll_app/employees.html', context)







def payslips(request):
    employees = Employee.objects.all()
    payslips = Payslip.objects.all()
    context = {
        'employees': employees,
        'payslips': payslips,
    }
    
    return render(request, 'payroll_app/payslips.html', context)

def create_payslip(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        pay_cycle = request.POST.get('cycle')
        id_number = request.POST.get('id_number')
        capitalized_month = month.title()

        if id_number == 'all_employees':
            employees = Employee.objects.all()
        else:
            employee = get_object_or_404(Employee, id_number=id_number)
            employees = [employee]

        for employee in employees:

            existing_payslip = Payslip.objects.filter(
                id_number=employee,
                month=month,
                year=year,
                pay_cycle=pay_cycle
            ).first()

            if existing_payslip:
                messages.error(request, f"Payslip already exists for Employee ID {employee.id_number}  for {capitalized_month} {year}, Cycle {pay_cycle}.")
                continue

            rate = employee.rate
            allowances = employee.allowance or 0
            overtime = employee.overtime_pay or 0
            pag_ibig = 100 if pay_cycle == '1' else 0
            deductions_health = 0
            sss = 0

            if pay_cycle == '1':
                taxable_amount = (rate / 2) + allowances + overtime - pag_ibig
                tax = taxable_amount * 0.2
                total_pay = taxable_amount - tax
            elif pay_cycle == '2':
                philhealth = rate * 0.04
                sss = rate * 0.045
                deductions_health = philhealth
                taxable_amount = (rate / 2) + allowances + overtime - deductions_health - sss
                tax = taxable_amount * 0.2
                total_pay = taxable_amount - tax

            if pay_cycle == '1':
                date_range = "1-15"
            elif pay_cycle == '2':
                months_with_30_days = ['April', 'June', 'September', 'November']
                if month.title() in months_with_30_days:
                    date_range = "16-30"
                elif month.title() == 'February':
                    date_range = "16-28"
                else:
                    date_range = "16-31"

            payslip = Payslip(
                id_number=employee,
                month=month,
                year=year,
                pay_cycle=pay_cycle,
                rate=rate,
                earnings_allowance=allowances,
                deductions_tax=tax,
                pag_ibig=pag_ibig,
                deductions_health=deductions_health,
                sss=sss,
                overtime=overtime,
                total_pay=total_pay,
                date_range=date_range
            )
            payslip.save()

            employee.overtime_pay = 0
            employee.save()
            messages.success(request, "Payslip successfully created.")

    return redirect('payslips')


def view_payslip(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)

    gross_pay = payslip.rate + payslip.earnings_allowance + payslip.overtime
    if payslip.pay_cycle == '1':
        total_deductions = payslip.deductions_tax + payslip.pag_ibig
    else:
        total_deductions = payslip.deductions_tax + payslip.deductions_health + payslip.sss


    context = {
        'payslip': payslip,
        'gross_pay': gross_pay,
        'total_deductions': total_deductions,
    }
    return render(request, 'payroll_app/view_payslip.html', context)

def delete_payslip(request, payslip_id):
    payslip = get_object_or_404(Payslip, id=payslip_id)
    
    if request.method == 'POST':
        payslip.delete()
        messages.success(request, 'Payslip deleted successfully.')
        return redirect('payslips')
    


def update_employee(request, id_number):
    employee = get_object_or_404(Employee, id_number=id_number)
    
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.id_number = request.POST['id_number']
        employee.rate = request.POST['rate']
        employee.allowance = request.POST.get('allowance', 0)
        
        employee.save()
        
        return redirect('employees')

    context = {
        'employee': employee,
    }
    return render(request, 'payroll_app/update_employee.html', context)

def delete_employee(request, id_number):
    if request.method == 'POST':
        employee = Employee.objects.filter(id_number=id_number).first()
        
        if employee:
            employee.delete()
        
        return redirect(reverse('employees'))

    return render(request, 'payroll_app/employees.html', {'error': 'Invalid request method'})
