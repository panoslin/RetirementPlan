#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
"""
OUTPUT:
RATE_YEARLY_GROWTH_SALARY
OR
RATE_YEARLY_GROWTH_PORTFOLIO

"""
__package__ = 'financial'
from .time_value_of_money import (
    nper,
    pv,
    fv,
    pmt,
    pmt_with_down_pmt,
)
from .utils import (
    str2datetime
)
import pandas as pd
import time
import datetime

date_of_now = datetime.datetime.now()

## DATE
__date_of_money_value = '2021/07/11'  # all the money value is based on this date
__date_of_birth = '1995/09/29'
__date_of_birth_spouse = '1997/03/22'
__date_of_birth_child = '2025/01/01'
__date_of_birth_parents = '1967/01/01'
__date_of_work = '2018/07/09'
__date_of_work_spouse = '2025/01/01'
__death_age = 90

date_of_money_value = str2datetime(__date_of_money_value)
date_of_birth = str2datetime(__date_of_birth)
date_of_birth_spouse = str2datetime(__date_of_birth_spouse)
date_of_birth_child = str2datetime(__date_of_birth_child)
date_of_birth_parents = str2datetime(__date_of_birth_parents)
date_of_work = str2datetime(__date_of_work)
date_of_work_spouse = str2datetime(__date_of_work_spouse)
date_of_death = date_of_birth + datetime.timedelta(days=365 * __death_age)

## EXPENSES
# LIVING
expense_monthly_food = 3500
expense_monthly_renting = 2000
expense_monthly_recreation = 1200
# WEDDING
age_of_wedding = 29
expense_wedding = 200000
# CAR
age_of_car = 30
__loan_term_car = 5
__percentage_first_pmt_car = 0.14
expense_car = 250000
# HOUSING
age_of_housing = 37
__price_per_square = 70000
__area = 150
__price_per_decoration = 6000
__loan_term_housing = 30
__percentage_first_pmt_housing = 0.3
expense_housing = (__price_per_square + __price_per_decoration) * __area
# PARENTS NURSING
age_of_nursing = 70
__expense_monthly_single_nursing = 15000
expense_monthly_nursing = __expense_monthly_single_nursing * 4
# RETIREMENT
age_of_retirement = 60
expense_monthly_couple = 20000

## INCOME/SAVING
income_monthly = 20000
saving = 27485
income_monthly_spouse = 5000
max_income_monthly = 100000

## RATE
INFLATION = 0.05
RATE_YEARLY_GROWTH_SALARY = 0.15
RATE_YEARLY_GROWTH_PORTFOLIO = 0.15
RATE_HOUSING_LOAD = 0.07
RATE_CAR_LOAD = 0.07

# calculate the money value to date_of_now.year
money_value = lambda x: pv(INFLATION, nper(date_of_money_value.year), 0, x)

def cal__expense_couple(year, expense):
    """
    double the expense if married
    :return:
    """
    age = year - date_of_birth.year
    if age < age_of_wedding:
        return expense
    else:
        return 2 * expense

def build_data(

) -> pd.DataFrame:
    # years scale from work to death
    time_scale = range(date_of_work.year, date_of_death.year + 1)

    df_timeframe = pd.DataFrame(
        {
            "year": year,
            "age": year - date_of_birth.year,
            "age_spouse": year - date_of_birth_spouse.year,
            "age_child": year - date_of_birth_child.year
            if year >= date_of_birth_child.year
            else None,
            "age_parents": int(year - date_of_birth_parents.year),
            # years till now
            "nper": nper(year),

        }
        for year in time_scale
    )

    # the value should base on the current year inflation
    df_expense = pd.DataFrame(
        {
            "year": year,
            "expense_food": cal__expense_couple(year, money_value(expense_monthly_food)),
            "expense_renting": cal__expense_couple(year, money_value(expense_monthly_renting))
            if year - date_of_birth.year <= age_of_housing
            else 0,
            "expense_recreation": cal__expense_couple(year, money_value(expense_monthly_recreation)),
            "expense_wedding": -pmt_with_down_pmt(
                year=year,
                start_year=date_of_birth.year + age_of_wedding,
                end_year=date_of_birth.year + age_of_wedding + 1,
                loan_rate=0,
                down_pmt_percentage=0,
                amount=money_value(expense_wedding)
            ),
            "expense_car": -pmt_with_down_pmt(
                year=year,
                start_year=date_of_birth.year + age_of_car,
                end_year=date_of_birth.year + age_of_car + __loan_term_car,
                loan_rate=RATE_CAR_LOAD,
                down_pmt_percentage=__percentage_first_pmt_car,
                amount=money_value(expense_car)
            ),
            "expense_housing": -pmt_with_down_pmt(
                year=year,
                start_year=date_of_birth.year + age_of_housing,
                end_year=date_of_birth.year + age_of_housing + __loan_term_housing,
                loan_rate=RATE_HOUSING_LOAD,
                down_pmt_percentage=__percentage_first_pmt_housing,
                amount=money_value(expense_housing)
            ),
            "expense_nursing": -expense_monthly_nursing
            if date_of_birth_parents.year + age_of_nursing <= year < (date_of_birth_parents + datetime.timedelta(days=365 * (__death_age + 5))).year
            else 0,
        }
        for year in time_scale
    )

    return pd.DataFrame()


if __name__ == '__main__':
    build_data(

    )
