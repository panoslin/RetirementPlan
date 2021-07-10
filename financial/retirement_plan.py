#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm

from .time_value_of_money import (
    pv,
    fv,
    pmt
)
import pandas as pd
import time
import datetime

date_of_now = datetime.datetime.now()

## DATE
str2datetime = lambda x: datetime.datetime.fromtimestamp(
    time.mktime(
        time.strptime(
            x,
            '%Y/%m/%d'
        )
    )
)
__date_of_birth = '1995/09/29'
__date_of_birth_spouse = '1997/03/22'
__date_of_birth_child = '2025/01/01'
__date_of_birth_parents = '1967/01/01'
__date_of_work = '2018/07/09'
__date_of_work_spouse = '2025/01/01'
__death_age = 90

date_of_birth = str2datetime(__date_of_birth)
date_of_birth_spouse = str2datetime(__date_of_birth_spouse)
date_of_birth_child = str2datetime(__date_of_birth_child)
date_of_birth_parents = str2datetime(__date_of_birth_parents)
date_of_work = str2datetime(__date_of_work)
date_of_work_spouse = str2datetime(__date_of_work_spouse)
date_of_death = date_of_birth + datetime.timedelta(days=365 * __death_age)

## EXPENSES
# LIVING
expense_monthly_food = 3473
expense_monthly_renting = 1985
expense_monthly_recreation = 1103
# WEDDING
age_of_wedding = 29
expense_wedding = 200000
# CAR
age_of_car = 30
expense_car = 250000
# HOUSING
age_of_housing = 37
__price_per_square = 70000
__area = 150
__price_per_decoration = 6000
__loan_term = 30
__percentage_first_pmt = 0.3
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

## LOAD
pmt_housing = pmt(
    RATE_HOUSING_LOAD / 12,
    __loan_term * 12,
    fv(
        INFLATION,
        age_of_housing - date_of_now.year,
        0,
        expense_housing * (1 - __percentage_first_pmt)
    )
)


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
            "nper": year - date_of_now.year,

        }
        for year in time_scale
    )

    df_expense = pd.DataFrame(
        {
            "year": year,
            "expense_food": fv(INFLATION, year - date_of_now.year, 0, expense_monthly_food),
            "expense_renting": fv(INFLATION, year - date_of_now.year, 0, expense_monthly_renting),
            "expense_recreation": fv(INFLATION, year - date_of_now.year, 0, expense_monthly_recreation),
            "expense_wedding": fv(INFLATION, year - date_of_now.year, 0, expense_wedding) / 12
            if year - date_of_birth.year == age_of_wedding
            else None,
            "expense_car": fv(INFLATION, year - date_of_now.year, 0, expense_car) / 12
            if year - date_of_birth.year == age_of_car
            else None,
            "expense_housing": pmt_housing
            if age_of_housing <= year - date_of_birth.year <= age_of_housing + __loan_term
            else None,

        }
        for year in time_scale
    )
    # df_expense = df_expense.merge(
    #     df_timeframe,
    #     how='left',
    #     on='year'
    # )

    return pd.DataFrame()


if __name__ == '__main__':
    build_data(

    )
