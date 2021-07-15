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


class Retirement(TimeValue):

    def __init__(
            self,
    ):

        ## RATE
        self.INFLATION = 0.05
        self.RATE_YEARLY_GROWTH_SALARY = 0.15
        self.RATE_YEARLY_GROWTH_PORTFOLIO = 0.15
        self.RATE_HOUSING_LOAD = 0.07
        self.RATE_CAR_LOAD = 0.07
        self.RATE_ESCALATION_LIVING = 0.05


        ## DATE
        __date_of_money_value = '2021/07/11'  # all the money value is based on this date
        __date_of_birth = '1995/09/29'
        __date_of_birth_spouse = '1997/03/22'
        __date_of_birth_child = '2025/01/01'
        __date_of_birth_parents = '1967/01/01'
        __date_of_work = '2018/07/09'
        __date_of_work_spouse = '2025/01/01'
        self.__death_age = 100

        self.date_of_now = datetime.datetime.now()
        self.date_of_money_value = str2datetime(__date_of_money_value)
        self.date_of_birth = str2datetime(__date_of_birth)
        self.date_of_birth_spouse = str2datetime(__date_of_birth_spouse)
        self.date_of_birth_child = str2datetime(__date_of_birth_child)
        self.date_of_birth_parents = str2datetime(__date_of_birth_parents)
        self.date_of_work = str2datetime(__date_of_work)
        self.date_of_work_spouse = str2datetime(__date_of_work_spouse)
        self.date_of_death = self.date_of_birth + datetime.timedelta(days=365 * self.__death_age)


        ## EXPENSES
        # LIVING
        __expense_monthly_food = 3500
        __max_expense_monthly_food = 13500
        __expense_monthly_renting = 2000
        __max_expense_monthly_renting = 15000
        __expense_monthly_recreation = 1200
        __max_expense_monthly_recreation = 12000

        self.expense_monthly_food = self.money_value(__expense_monthly_food)
        self.max_expense_monthly_food = self.money_value(__max_expense_monthly_food)
        self.expense_monthly_renting = self.money_value(__expense_monthly_renting)
        self.max_expense_monthly_renting = self.money_value(__max_expense_monthly_renting)
        self.expense_monthly_recreation = self.money_value(__expense_monthly_recreation)
        self.max_expense_monthly_recreation = self.money_value(__max_expense_monthly_recreation)

        # WEDDING
        __age_of_wedding = 29

        self.age_of_wedding = __age_of_wedding
        self.expense_wedding = self.money_value(200000)

        # CAR
        __age_of_car = 30

        self.loan_term_car = 5
        self.percentage_first_pmt_car = 0.14
        self.age_of_car = __age_of_car
        self.expense_car = self.money_value(250000)

        # HOUSING
        __age_of_housing = 37
        __price_per_square = 70000
        __area = 150
        __price_per_decoration = 6000

        self.loan_term_housing = 30
        self.percentage_first_pmt_housing = 0.3
        self.age_of_housing = __age_of_housing
        self.expense_housing = self.money_value(
            (__price_per_square + __price_per_decoration) * __area
        )

        # PARENTS NURSING
        __age_of_nursing = 70
        __expense_monthly_single_nursing = 20000

        self.expense_monthly_single_nursing = __expense_monthly_single_nursing
        self.age_of_nursing = __age_of_nursing
        self.expense_monthly_nursing = self.expense_monthly_single_nursing * 4

        # RETIREMENT
        __age_of_retirement = 60
        __expense_monthly_pension_couple = 20000

        self.age_of_retirement = __age_of_retirement
        self.expense_monthly_pension_couple = self.money_value(__expense_monthly_pension_couple)

        ## INCOME/SAVING
        __income_monthly = 20000
        __saving = 27485
        __income_monthly_spouse = 5000
        __max_income_monthly = 50000


        self.income_monthly = self.money_value(__income_monthly)
        self.saving = self.money_value(__saving)
        self.income_monthly_spouse = self.money_value(__income_monthly_spouse)
        self.max_income_monthly = self.money_value(__max_income_monthly)

    def money_value(self, amount):
        """
        Calculate the money value to date_of_now.year
        """
        return self.pv(
            rate=self.INFLATION,
            nper=self.nper(self.date_of_money_value.year),
            pmt=0,
            fv=amount
        )

    def cal__expense_couple(self, year, expense, maximum, multiplier=2):
        """
        Multiply the expense if married
        :return:
        """
        age = year - self.date_of_birth.year
        expense = -self.cal__growth_flow(
            year=year,
            rate=self.RATE_ESCALATION_LIVING,
            amount=-expense,
            maximum=maximum
        )
        if age < self.age_of_wedding:
            return expense
        else:
            return multiplier * expense

    def cal__growth_flow(
            self,
            year,
            rate,
            amount,
            maximum=sys.maxsize
    ):
        """
        Calculte a series of cash flows grow with time
        :param year:
        :param rate:
        :param amount:
        :param maximum:
        :return:
        """
        growth_amount = amount * (1 + rate) ** self.nper(year)
        return growth_amount if abs(growth_amount) <= abs(maximum) else maximum

    def build__df_time_frame(self, time_scale):
        df_timeframe = pd.DataFrame(
            {
                "year": year,
                "age": year - self.date_of_birth.year,
                "age_spouse": year - self.date_of_birth_spouse.year,
                "age_child": year - self.date_of_birth_child.year
                if year >= self.date_of_birth_child.year
                else 0,
                "age_parents": int(year - self.date_of_birth_parents.year),
                # years till now
                # "nper": nper(year),

            }
            for year in time_scale
        )
        return df_timeframe

    def build__df_expense(self, time_scale):
        df_expense = pd.DataFrame(
            {
                "year": year,
                "expense_food": self.cal__expense_couple(
                    year=year,
                    expense=self.expense_monthly_food,
                    maximum=self.max_expense_monthly_food
                ),
                "expense_renting": self.cal__expense_couple(
                    year=year,
                    expense=self.expense_monthly_renting,
                    maximum=self.max_expense_monthly_renting,
                    multiplier=3
                )
                if year - self.date_of_birth.year <= self.age_of_housing
                else 0,
                "expense_recreation": self.cal__expense_couple(
                    year=year,
                    expense=self.expense_monthly_recreation,
                    maximum=self.max_expense_monthly_recreation
                ),
                "expense_wedding": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth.year + self.age_of_wedding,
                    end_year=self.date_of_birth.year + self.age_of_wedding + 1,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=self.expense_wedding
                ),
                "expense_car": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth.year + self.age_of_car,
                    end_year=self.date_of_birth.year + self.age_of_car + self.loan_term_car,
                    loan_rate=self.RATE_CAR_LOAD,
                    down_pmt_percentage=self.percentage_first_pmt_car,
                    amount=self.expense_car
                ),
                "expense_housing": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth.year + self.age_of_housing,
                    end_year=self.date_of_birth.year + self.age_of_housing + self.loan_term_housing,
                    loan_rate=self.RATE_HOUSING_LOAD,
                    down_pmt_percentage=self.percentage_first_pmt_housing,
                    amount=self.expense_housing
                ),
                "expense_nursing": -self.expense_monthly_nursing
                if self.date_of_birth_parents.year + self.age_of_nursing <= year < (
                        self.date_of_birth_parents + datetime.timedelta(days=365 * (self.__death_age + 5))).year
                else 0,
                "expense_pension": self.expense_monthly_pension_couple
                if year >= self.date_of_birth.year + self.age_of_retirement
                else 0
            }
            for year in time_scale
        )
        df_expense['expense_total'] = df_expense.iloc[:, 1:].sum(axis=1)
        return df_expense

    def build__df_income(self, time_scale):
        df_income = pd.DataFrame(
            {
                "year": year,
                "income": self.cal__growth_flow(
                    year=year,
                    rate=self.RATE_YEARLY_GROWTH_SALARY,
                    amount=-self.income_monthly,
                    maximum=-self.max_income_monthly,
                ) if self.date_of_work.year <= year < self.date_of_birth.year + self.age_of_retirement else 0,
                "income_spouse": self.cal__growth_flow(
                    year=year,
                    rate=self.RATE_YEARLY_GROWTH_SALARY,
                    amount=-self.income_monthly_spouse,
                    maximum=-self.max_income_monthly,
                ) if self.date_of_work_spouse.year <= year < self.date_of_birth_spouse.year + self.age_of_retirement else 0,
            }
            for year in time_scale
        )
        df_income['income_total'] = df_income.iloc[:, 1:].sum(axis=1)
        return df_income

    def cal__expense_nursing(self, df):
        """
        Parents nursing expense and the couple's
        """
        df['expense_nursing'] = df.apply(
            lambda x: x['expense_nursing'] - self.expense_monthly_single_nursing
            if x['age'] >= self.age_of_nursing else x['expense_nursing'],
            axis=1
        )
        df['expense_nursing'] = df.apply(
            lambda x: x['expense_nursing'] - self.expense_monthly_single_nursing
            if x['age_spouse'] >= self.age_of_nursing else x['expense_nursing'],
            axis=1
        )

    def cal__saving(self, df):
        """
        Calculte cummulative saving
        """
        df['saving'] = 0
        # current saving
        df.loc[df['year'] == self.date_of_money_value.year, 'saving'] = -self.saving
        previous_saving = 0

        def cal__saving(currnet_row):
            nonlocal previous_saving
            if currnet_row['year'] < self.date_of_now.year:
                return 0
            elif currnet_row['year'] == self.date_of_now.year:
                # current saving with interest + rest of the saving of the year with interest
                current_saving = -self.fv(
                    self.RATE_YEARLY_GROWTH_PORTFOLIO/12,
                    12 - self.date_of_now.month,
                    0,
                    currnet_row['saving']
                ) - self.fv(
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12,
                    12 - self.date_of_now.month,
                    currnet_row['income_total'] + currnet_row['expense_total']
                )
                previous_saving = current_saving
                return current_saving
            else:
                # previous saving with interest + year's of saving with interest
                current_saving = -self.fv(
                    self.RATE_YEARLY_GROWTH_PORTFOLIO/12,
                    12,
                    0,
                    previous_saving
                ) - self.fv(
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12,
                    12,
                    currnet_row['income_total'] + currnet_row['expense_total']
                )
                previous_saving = current_saving
                return current_saving

        df['saving'] = df.apply(
            cal__saving,
            axis=1
        )

    def build_data(
            self,
            detail=False
    ) -> pd.DataFrame:
        """
        Build up cash flow DataFrame
        """

        # years scale from work to death
        time_scale = range(self.date_of_work.year, self.date_of_death.year + 1)

        df_timeframe = self.build__df_time_frame(time_scale)

        # the values are base on the current year's inflation
        df_expense = self.build__df_expense(time_scale)

        df_income = self.build__df_income(time_scale)

        # merge df's
        df = df_timeframe.merge(
            df_expense if detail else df_expense[['year', 'expense_total']],
            on='year'
        )
        df = df.merge(
            df_income if detail else df_income[['year', 'income_total']],
            on='year'
        )

        del df_timeframe, df_expense, df_income, time_scale

        self.cal__expense_nursing(df)

        self.cal__saving(df)

        return df


if __name__ == '__main__':
    plan = Retirement()
    plan.build_data(
        detail=True
    )