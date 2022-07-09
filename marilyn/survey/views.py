from django.shortcuts import render
from .forms import FinancialPlanForm
from django.http import HttpResponse
from financial.retirement_plan import Retirement
from uuid import uuid1
import os
import datetime


def index(request):
    if request.method == 'POST':
        form = FinancialPlanForm(request.POST)
        if form.is_valid():
            return report(form)
        else:
            return HttpResponse('invalid!')

    context = {'form': FinancialPlanForm()}
    return render(request, 'survey/index.html', context)


def report(form):
    plan = Retirement(
        datetime.datetime.now(),
        form.cleaned_data['date_of_birth'],
        form.cleaned_data['date_of_birth_spouse'],
        form.cleaned_data['date_of_birth_child'],
        form.cleaned_data['date_of_birth_parents'],
        form.cleaned_data['date_of_work'],
        form.cleaned_data['date_of_work_spouse'],
        form.cleaned_data['age_of_wedding'],
        form.cleaned_data['age_of_car'],
        form.cleaned_data['age_of_housing'],
        form.cleaned_data['price_per_square'],
        form.cleaned_data['area'],
        form.cleaned_data['price_per_decoration'],
        70,
        20000,
        form.cleaned_data['age_of_retirement'],
        form.cleaned_data['expense_monthly_pension_couple'],
        form.cleaned_data['income_monthly'],
        form.cleaned_data['saving'],
        form.cleaned_data['income_monthly_spouse'],
        form.cleaned_data['max_income_monthly'],
        form.cleaned_data['expense_monthly_food'],
        form.cleaned_data['max_expense_monthly_food'],
        form.cleaned_data['expense_monthly_renting'],
        form.cleaned_data['max_expense_monthly_renting'],
        form.cleaned_data['expense_monthly_recreation'],
        form.cleaned_data['max_expense_monthly_recreation'],
        form.cleaned_data['expense_wedding'],
        form.cleaned_data['expense_car'],
    )
    otires = plan.optimize()
    if not otires.success:
        return HttpResponse(
            'Sorry, the algorithm cannot find a reasonable solution\n'
            'Please lower the expense or higher the income'
        )
    plan.RATE_YEARLY_GROWTH_PORTFOLIO = plan.RATE_YEARLY_GROWTH_SALARY = otires.x[0]
    temp_report_dir = '.temp_report_dir'
    os.makedirs(temp_report_dir, exist_ok=True)
    report_name = f"{temp_report_dir}/{uuid1().hex}.xlsx"
    plan.build__report(report_name=report_name)
    return response__excel(report_name)


def response__excel(excel):
    with open(excel, "rb") as file:
        response = HttpResponse(
            file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(excel)}'
        return response
