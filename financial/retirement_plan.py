#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
"""
OUTPUT:
RATE_YEARLY_GROWTH_SALARY
OR
RATE_YEARLY_GROWTH_PORTFOLIO

and csv file

"""
from pathlib import Path

import sys

__package__ = Path(__file__).parent.stem

from .time_value_of_money import TimeValue
from .utils import (
    str2datetime
)
import pandas as pd
import datetime

date_of_now = datetime.datetime.now()

## DATE
__date_of_money_value = '***REMOVED***'  # all the money value is based on this date
__date_of_birth = '1995/09/***REMOVED***'
__date_of_birth_spouse = '***REMOVED***'
__date_of_birth_child = '***REMOVED***'
__date_of_birth_parents = '***REMOVED***'
__date_of_work = '***REMOVED***'
__date_of_work_spouse = '***REMOVED***'
__death_age = 100

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
expense_monthly_food = ***REMOVED***
max_expense_monthly_food = 1***REMOVED***
expense_monthly_renting = ***REMOVED***
max_expense_monthly_renting = ***REMOVED***00
expense_monthly_recreation = ***REMOVED***
max_expense_monthly_recreation = 1***REMOVED***
# WEDDING
age_of_wedding = ***REMOVED***
expense_wedding = ***REMOVED***
# CAR
age_of_car = ***REMOVED***
__loan_term_car = 5
__percentage_first_pmt_car = 0.14
expense_car = ***REMOVED***
# HOUSING
age_of_housing = ***REMOVED***
__price_per_square = ***REMOVED***000
__area = ***REMOVED***
__price_per_decoration = ***REMOVED***00
__loan_term_housing = ***REMOVED***
__percentage_first_pmt_housing = 0.3
expense_housing = (__price_per_square + __price_per_decoration) * __area
# PARENTS NURSING
age_of_nursing = ***REMOVED***
__expense_monthly_single_nursing = ***REMOVED***0
expense_monthly_nursing = __expense_monthly_single_nursing * 4
# RETIREMENT
age_of_retirement = ***REMOVED***
expense_monthly_pension_couple = ***REMOVED***0

## INCOME/SAVING
income_monthly = ***REMOVED***0
saving = ***REMOVED***
income_monthly_spouse = ***REMOVED***
max_income_monthly = ***REMOVED***

## RATE
INFLATION = 0.05
RATE_YEARLY_GROWTH_SALARY = 0.15
RATE_YEARLY_GROWTH_PORTFOLIO = 0.15
RATE_HOUSING_LOAD = 0.07
RATE_CAR_LOAD = 0.07
RATE_ESCALATION_LIVING = 0.05

# calculate the money value to date_of_now.year
money_value = lambda x: TimeValue.pv(INFLATION, TimeValue.nper(date_of_money_value.year), 0, x)


def cal__expense_couple(year, expense, maximum):
    """
    double the expense if married
    :return:
    """
    age = year - date_of_birth.year
    expense = -cal__growth_flow(
        year=year,
        rate=RATE_ESCALATION_LIVING,
        amount=-expense,
        maximum=maximum
    )
    if age < age_of_wedding:
        return expense
    else:
        return 2 * expense


def cal__growth_flow(
        year,
        rate,
        amount,
        maximum=sys.maxsize
):
    growth_amount = amount * (1 + rate) ** TimeValue.nper(year)
    return growth_amount if abs(growth_amount) <= abs(maximum) else maximum

# def cal__nursing(
#         year,
#
# ):
#     if (
#             date_of_birth_parents.year + age_of_nursing
#             <= year
#             < (date_of_birth_parents + datetime.timedelta(days=365 * __death_age)).year
#     ):
#         return -expense_monthly_nursing
#     elif year >= date_of_birth.year + age_of_nursing:
#         return __expense_monthly_single_nursing * 2
#     else:
#         return 0

def build_data(
    detail=False
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
            else 0,
            "age_parents": int(year - date_of_birth_parents.year),
            # years till now
            # "nper": nper(year),

        }
        for year in time_scale
    )

    # the value should base on the current year inflation
    # TODO: escalation of food and recreation (pursuing of better life quality)
    df_expense = pd.DataFrame(
        {
            "year": year,
            "expense_food": cal__expense_couple(
                year=year,
                expense=money_value(expense_monthly_food),
                maximum=max_expense_monthly_food
            ),
            "expense_renting": cal__expense_couple(
                year=year,
                expense=money_value(expense_monthly_renting),
                maximum=max_expense_monthly_renting
            )
            if year - date_of_birth.year <= age_of_housing
            else 0,
            "expense_recreation": cal__expense_couple(
                year=year,
                expense=money_value(expense_monthly_recreation),
                maximum=max_expense_monthly_recreation
            ),
            "expense_wedding": -TimeValue.pmt_with_down_pmt(
                year=year,
                start_year=date_of_birth.year + age_of_wedding,
                end_year=date_of_birth.year + age_of_wedding + 1,
                loan_rate=0,
                down_pmt_percentage=0,
                amount=money_value(expense_wedding)
            ),
            "expense_car": -TimeValue.pmt_with_down_pmt(
                year=year,
                start_year=date_of_birth.year + age_of_car,
                end_year=date_of_birth.year + age_of_car + __loan_term_car,
                loan_rate=RATE_CAR_LOAD,
                down_pmt_percentage=__percentage_first_pmt_car,
                amount=money_value(expense_car)
            ),
            "expense_housing": -TimeValue.pmt_with_down_pmt(
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
            "expense_pension": money_value(expense_monthly_pension_couple)
            if year >= date_of_birth.year + age_of_retirement
            else 0
        }
        for year in time_scale
    )
    df_expense['expense_total'] = df_expense.iloc[:, 1:].sum(axis=1)

    # TODO: INCOME DF
    df_income = pd.DataFrame(
        {
            "year": year,
            "income": cal__growth_flow(
                year=year,
                rate=RATE_YEARLY_GROWTH_SALARY,
                amount=-money_value(income_monthly),
                maximum=-money_value(max_income_monthly),
            ) if date_of_work.year <= year < date_of_birth.year + age_of_retirement else 0,
            "income_spouse": cal__growth_flow(
                year=year,
                rate=RATE_YEARLY_GROWTH_SALARY,
                amount=-money_value(income_monthly_spouse),
                maximum=-money_value(max_income_monthly),
            ) if date_of_work_spouse.year <= year < date_of_birth_spouse.year + age_of_retirement else 0,
        }
        for year in time_scale
    )
    df_income['income_total'] = df_income.iloc[:, 1:].sum(axis=1)

    # merge df's
    df = df_timeframe.merge(
        df_expense if detail else df_expense[['year', 'expense_total']] ,
        on='year'
    )
    df = df.merge(
        df_income if detail else df_income[['year', 'income_total']],
        on='year'
    )

    del df_timeframe, df_expense, df_income, time_scale


    # calculate nursing
    df['expense_nursing'] = df.apply(
        lambda x:x['expense_nursing'] - __expense_monthly_single_nursing
        if x['age'] >= age_of_nursing else x['expense_nursing'],
        axis=1
    )
    df['expense_nursing'] = df.apply(
        lambda x:x['expense_nursing'] - __expense_monthly_single_nursing
        if x['age_spouse'] >= age_of_nursing else x['expense_nursing'],
        axis=1
    )

    # calculte saving
    df['saving'] = 0
    df.loc[df['year'] == date_of_money_value.year, 'saving'] = -money_value(saving)
    previous_saving = 0

    def cal__saving(currnet_row):
        nonlocal previous_saving
        if currnet_row['year'] < date_of_now.year:
            return 0
        elif currnet_row['year'] == date_of_now.year:
            # current saving + rest of the saving of the year with interest
            current_saving = currnet_row['saving'] - TimeValue.fv(
                RATE_YEARLY_GROWTH_PORTFOLIO / 12,
                12 - date_of_now.month,
                currnet_row['income_total'] + currnet_row['expense_total']
            )
            previous_saving = current_saving
            return current_saving
        else:
            # previous saving with interest + year's of saving with interest
            current_saving = previous_saving * (1 + RATE_YEARLY_GROWTH_PORTFOLIO) - TimeValue.fv(
                RATE_YEARLY_GROWTH_PORTFOLIO / 12,
                12,
                currnet_row['income_total'] + currnet_row['expense_total']
            )
            previous_saving = current_saving
            return current_saving

    df['saving'] = df.apply(
        cal__saving,
        axis=1
    )
    del previous_saving

    return df


if __name__ == '__main__':
    build_data(
        detail=True
    )
