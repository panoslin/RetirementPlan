#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/8/1
# IDE: PyCharm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div


class DateInput(forms.DateInput):
    input_type = 'date'


class FinancialPlanForm(forms.Form):
    date_of_birth = forms.DateField(
        required=True,
        widget=DateInput,
        label='1. Birthdate',
    )
    date_of_birth_spouse = forms.DateField(
        required=True,
        widget=DateInput,
        label='2. Birthdate of spouse',
    )
    date_of_birth_parents = forms.DateField(
        required=True,
        widget=DateInput,
        label='3. Birthdate of the oldest parent',
    )
    date_of_birth_child = forms.DateField(
        required=False,
        widget=DateInput,
        label='4. Birthdate of child (expected)',
    )
    date_of_work = forms.DateField(
        required=False,
        widget=DateInput,
        label='5. The date start to make money',
    )
    date_of_work_spouse = forms.DateField(
        required=False,
        widget=DateInput,
        label='6. The date start to make money (spouse)',
    )

    income_monthly = forms.IntegerField(
        required=True,
        initial=10000,
        label='7. Current salary (monthly)',
        help_text='Expected salary if not work yet',
    )
    income_monthly_spouse = forms.IntegerField(
        required=True,
        initial=10000,
        label='8. Current salary from spouse (monthly)',
        help_text='Expected salary if not work yet',
    )
    max_income_monthly = forms.IntegerField(
        required=True,
        initial=50000,
        label='9. Expected maximum monthly salary',
    )
    saving = forms.IntegerField(
        required=True,
        label='10. Current financial assets amount',
        help_text='Including Cash, stocks, bonds, and bank deposits'
    )

    expense_monthly_food = forms.IntegerField(
        required=True,
        initial=3000,
        label='11. Monthly expense on food',
    )
    max_expense_monthly_food = forms.IntegerField(
        required=True,
        initial=10000,
        label='12. Maximum Monthly expense on food',
    )
    expense_monthly_renting = forms.IntegerField(
        required=True,
        initial=5000,
        label='13. Monthly expense on rent',
    )
    max_expense_monthly_renting = forms.IntegerField(
        required=True,
        initial=15000,
        label='14. Maximum Monthly expense on rent',
    )
    expense_monthly_recreation = forms.IntegerField(
        required=True,
        initial=2000,
        label='15. Monthly expense on recreation',
    )
    max_expense_monthly_recreation = forms.IntegerField(
        required=True,
        initial=20000,
        label='16. Maximum Monthly expense on recreation',
    )

    age_of_wedding = forms.IntegerField(
        required=True,
        initial=28,
        label='17. Age of marriage (expected)',
        min_value=22,
        max_value=100,
    )
    expense_wedding = forms.IntegerField(
        required=True,
        initial=500000,
        label='18. Expense of wedding ceremony',
    )
    age_of_car = forms.IntegerField(
        required=True,
        initial=28,
        label='19. Age of having a car',
        min_value=18,
        max_value=100,
    )
    expense_car = forms.IntegerField(
        required=True,
        initial=300000,
        label='20. Expense of purchasing a car',
    )
    age_of_housing = forms.IntegerField(
        required=True,
        initial=30,
        label='21. Age of having a house',
        max_value=100,
    )
    price_per_square = forms.IntegerField(
        required=True,
        initial=50000,
        label='22. Price per squere meter',
    )
    price_per_decoration = forms.IntegerField(
        required=True,
        initial=10000,
        label='23. Price per squere meter (decoration)',
    )
    area = forms.IntegerField(
        required=True,
        initial=150,
        label='24. Size of the house (square meter)',
    )

    age_of_retirement = forms.IntegerField(
        required=True,
        initial=60,
        label='25. Expected retiring age',
    )
    expense_monthly_pension_couple = forms.IntegerField(
        required=True,
        initial=20000,
        label='26. Expected monthly expense after retirement (couple)',
    )
    
    

    def __init__(self, *args, **kwargs):
        super(FinancialPlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'row'
        self.helper.label_class = 'title-label'
        # self.helper.field_class = 'col-sm'
        self.helper.layout = Layout(
            'date_of_birth',
            'date_of_birth_spouse',
            'date_of_birth_child',
            'date_of_birth_parents',
            'date_of_work',
            'date_of_work_spouse',

            'income_monthly',
            'income_monthly_spouse',
            'max_income_monthly',
            'saving',
            
            'expense_monthly_food',
            'max_expense_monthly_food',
            'expense_monthly_renting',
            'max_expense_monthly_renting',
            'expense_monthly_recreation',
            'max_expense_monthly_recreation',
            
            'age_of_wedding',
            'expense_wedding',
            'age_of_car',
            'expense_car',
            'age_of_housing',
            'price_per_square',
            'price_per_decoration',
            'area',
            
            'age_of_retirement',
            'expense_monthly_pension_couple',
            
            Div(
                Submit('submit', 'Generate Financial Statements', css_class='btn-green'),
            )
        )
