#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
import pandas as pd
import time
import datetime
from time_value_of_money import (
    pv,
    fv,
    pmt
)

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
__date_of_birth = '***REMOVED***'
__date_of_birth_spouse = '***REMOVED***'
__date_of_birth_child = '***REMOVED***'
__date_of_birth_parents = '***REMOVED***'
__date_of_work = '***REMOVED***'
__date_of_work_spouse = '***REMOVED***'
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
age_of_wedding = ***REMOVED***
expense_wedding = ***REMOVED***0
# CAR
age_of_car = ***REMOVED***
expense_car = 2***REMOVED***0
# HOUSING
age_of_housing = ***REMOVED***
__price_per_square = ***REMOVED***
__area = ***REMOVED***
__price_per_decoration = ***REMOVED***
__loan_term = ***REMOVED***
__percentage_first_pmt = 0.3
expense_housing = (__price_per_square + __price_per_decoration) * __area
# PARENTS NURSING
age_of_nursing = ***REMOVED***
__expense_monthly_single_nursing = ***REMOVED***00
expense_monthly_nursing = __expense_monthly_single_nursing * 4
# RETIREMENT
age_of_retirement = ***REMOVED***
expense_monthly_couple = ***REMOVED***

## INCOME/SAVING
income_monthly = ***REMOVED***
saving = ***REMOVED***
income_monthly_spouse = ***REMOVED***
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
