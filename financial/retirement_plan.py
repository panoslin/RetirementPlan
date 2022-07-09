#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
"""
OUTPUT:
RATE_YEARLY_GROWTH_SALARY
OR
RATE_YEARLY_GROWTH_PORTFOLIO
OR
max_income_monthly

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
import numpy as np
from scipy import optimize
from typing import Callable


class Retirement(TimeValue):

    def __init__(
            self,
            __date_of_money_value='2021/07/11',  # all the money value is based on this date
            __date_of_birth='1995/01/01',
            __date_of_birth_spouse='1997/01/01',
            __date_of_birth_child='2025/01/01',
            __date_of_birth_parents='1965/01/01',
            __date_of_work='2018/01/01',
            __date_of_work_spouse='2020/01/01',
            __age_of_wedding=25,
            __age_of_car=25,
            __age_of_housing=30,
            __price_per_square=10000,
            __area=150,
            __price_per_decoration=6000,
            __age_of_nursing=70,
            __expense_monthly_single_nursing=20000,
            __age_of_retirement=70,
            __expense_monthly_pension_couple=20000,
            __income_monthly=10000,
            __saving=500000,
            __income_monthly_spouse=10000,
            __max_income_monthly=100000,
            __expense_monthly_food=3500,
            __max_expense_monthly_food=13500,
            __expense_monthly_renting=5000,
            __max_expense_monthly_renting=15000,
            __expense_monthly_recreation=2000,
            __max_expense_monthly_recreation=12000,
            __expense_wedding=500000,
            __expense_car=500000,

    ):

        ## RATE
        self.INFLATION = 0.05
        self.RATE_YEARLY_GROWTH_SALARY = 0.1716
        # including yield from money market, stock market, insurances and etc.
        self.RATE_YEARLY_GROWTH_PORTFOLIO = 0.1716
        self.RATE_HOUSING_LOAD = 0.07
        self.RATE_CAR_LOAN = 0.07
        self.RATE_ESCALATION_LIVING = 0.05

        ## DATE

        self.death_age = 100
        self.date_of_now = datetime.datetime.now()
        self.date_of_money_value = str2datetime(__date_of_money_value)
        self.date_of_birth = str2datetime(__date_of_birth)
        self.date_of_birth_spouse = str2datetime(__date_of_birth_spouse)
        self.date_of_birth_child = str2datetime(__date_of_birth_child)
        self.date_of_birth_parents = str2datetime(__date_of_birth_parents)
        self.date_of_work = str2datetime(__date_of_work)
        self.date_of_work_spouse = str2datetime(__date_of_work_spouse)
        self.date_of_death = self.date_of_birth + datetime.timedelta(days=365 * self.death_age)

        ## EXPENSES
        # LIVING

        self.expense_monthly_food = self.money_value(__expense_monthly_food)
        self.max_expense_monthly_food = self.money_value(__max_expense_monthly_food)
        self.expense_monthly_renting = self.money_value(__expense_monthly_renting)
        self.max_expense_monthly_renting = self.money_value(__max_expense_monthly_renting)
        self.expense_monthly_recreation = self.money_value(__expense_monthly_recreation)
        self.max_expense_monthly_recreation = self.money_value(__max_expense_monthly_recreation)

        # WEDDING
        self.age_of_wedding = __age_of_wedding
        self.expense_wedding = self.money_value(__expense_wedding)

        # CAR
        self.loan_term_car = 5
        self.percentage_first_pmt_car = 0.14
        self.age_of_car = __age_of_car
        self.expense_car = self.money_value(__expense_car)

        # HOUSING
        self.loan_term_housing = 30
        self.percentage_first_pmt_housing = 0.3
        self.age_of_housing = __age_of_housing
        self.expense_housing = self.money_value(
            (__price_per_square + __price_per_decoration) * __area
        )

        # PARENTS NURSING
        self.expense_monthly_single_nursing = __expense_monthly_single_nursing
        self.age_of_nursing = __age_of_nursing
        self.expense_monthly_nursing = self.expense_monthly_single_nursing * 4

        # RETIREMENT
        self.age_of_retirement = __age_of_retirement
        self.expense_monthly_pension_couple = self.money_value(__expense_monthly_pension_couple)

        ## INCOME/SAVING
        self.income_monthly = self.money_value(__income_monthly)
        self.saving = self.money_value(__saving)
        self.income_monthly_spouse = self.money_value(__income_monthly_spouse)
        self.max_income_monthly = self.money_value(__max_income_monthly)

        self.last_saving = None
        self.note = None

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

    def cal__expense_nursing(self, df):
        """
        Parents nursing expense and the couple's
        """
        df['expense_nursing'] = df.apply(
            lambda x: x['expense_nursing'] - self.expense_monthly_single_nursing
            if x['year'] - self.date_of_birth.year >= self.age_of_nursing else x['expense_nursing'],
            axis=1
        )
        df['expense_nursing'] = df.apply(
            lambda x: x['expense_nursing'] - self.expense_monthly_single_nursing
            if x['year'] - self.date_of_birth_spouse.year >= self.age_of_nursing else x['expense_nursing'],
            axis=1
        )

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
                    maximum=-self.max_expense_monthly_food
                ),
                "expense_renting": self.cal__expense_couple(
                    year=year,
                    expense=self.expense_monthly_renting,
                    maximum=-self.max_expense_monthly_renting,
                    multiplier=3
                )
                if year - self.date_of_birth.year <= self.age_of_housing + 1
                else 0,
                "expense_recreation": self.cal__expense_couple(
                    year=year,
                    expense=self.expense_monthly_recreation,
                    maximum=-self.max_expense_monthly_recreation
                ) * (
                    # reduce half of the recreation in the year of weding
                    0.5 if year == self.date_of_birth.year + self.age_of_wedding else 1
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
                    loan_rate=self.RATE_CAR_LOAN,
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
                if (
                        self.date_of_birth_parents.year + self.age_of_nursing
                        <= year
                        < (self.date_of_birth_parents + datetime.timedelta(days=365 * self.death_age)).year
                )
                else 0,
                "expense_pension": self.expense_monthly_pension_couple
                if year >= self.date_of_birth.year + self.age_of_retirement
                else 0,

                "expense_giving_birth": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year,
                    end_year=self.date_of_birth_child.year + 1,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-50000
                ),

                "expense_caring": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year,
                    end_year=self.date_of_birth_child.year + 1,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-500000
                ),
                "expense_edu_kindergarden": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 4,
                    end_year=self.date_of_birth_child.year + 4 + 3,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-60000
                ),
                "expense_edu_primary": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 6,
                    end_year=self.date_of_birth_child.year + 6 + 6,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-120000
                ),
                "expense_edu_mid": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 12,
                    end_year=self.date_of_birth_child.year + 12 + 3,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-120000
                ),
                "expense_edu_high": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 15,
                    end_year=self.date_of_birth_child.year + 15 + 3,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-120000
                ),
                "expense_edu_bachelor": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 18,
                    end_year=self.date_of_birth_child.year + 18 + 4,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-100000 * 4
                ),
                "expense_graduate_degree": -self.pmt_with_down_pmt(
                    year=year,
                    start_year=self.date_of_birth_child.year + 22,
                    end_year=self.date_of_birth_child.year + 22 + 2,
                    loan_rate=0,
                    down_pmt_percentage=0,
                    amount=-500000
                ),
            }
            for year in time_scale
        )
        self.cal__expense_nursing(df_expense)
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
                    maximum=abs(self.max_income_monthly),
                ) if self.date_of_work.year <= year < self.date_of_birth.year + self.age_of_retirement else 0,
                "income_spouse": self.cal__growth_flow(
                    year=year,
                    rate=self.RATE_YEARLY_GROWTH_SALARY,
                    amount=-self.income_monthly_spouse,
                    maximum=abs(self.max_income_monthly),
                ) if (
                        self.date_of_work_spouse.year <= year < self.date_of_birth_spouse.year + self.age_of_retirement
                        # excluding the year when child birth
                        and year != self.date_of_birth_child.year
                ) else 0,
            }
            for year in time_scale
        )
        df_income['income_total'] = df_income.iloc[:, 1:].sum(axis=1)
        return df_income

    def cal__saving(self, df: pd.DataFrame, detail):
        """
        Calculte cummulative saving
        """
        df['income_portfolio_annually'] = 0
        df['saving'] = 0
        # saving on money value date (the date filling in the data)
        if self.date_of_money_value.year >= self.date_of_work.year:
            previous_saving = -self.saving
        else:
            previous_saving = self.fv(
                self.RATE_YEARLY_GROWTH_PORTFOLIO
                if self.saving >= 0
                else self.INFLATION,
                self.date_of_work.year - self.date_of_money_value.year - 1,
                0,
                self.saving
            )

        def cal__saving(currnet_row):
            nonlocal previous_saving
            if currnet_row['year'] < self.date_of_money_value.year:
                return 0, 0
            elif currnet_row['year'] == self.date_of_money_value.year:
                # current saving with interest + rest of the saving of the year with interest
                previous_saving_with_interest = -self.fv(
                    # income
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12
                    if previous_saving >= 0
                    # loan
                    else self.INFLATION / 12,

                    12 - self.date_of_now.month,
                    0,
                    previous_saving
                )
                income_with_interest = - self.fv(
                    # income
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12
                    if currnet_row['income_total'] + currnet_row['expense_total'] >= 0
                    # loan
                    else self.INFLATION / 12,

                    12 - self.date_of_now.month,
                    currnet_row['income_total'] + currnet_row['expense_total']
                )
                current_saving = previous_saving_with_interest + income_with_interest
                income_portfolio = previous_saving_with_interest - previous_saving
                previous_saving = current_saving
                return income_portfolio, current_saving
            else:
                # previous saving with interest + year's of saving with interest
                previous_saving_with_interest = -self.fv(
                    # income
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12
                    if previous_saving >= 0
                    # loan
                    else self.INFLATION / 12,
                    12,
                    0,
                    previous_saving
                )
                income_with_interest = - self.fv(
                    # income
                    self.RATE_YEARLY_GROWTH_PORTFOLIO / 12
                    if currnet_row['income_total'] + currnet_row['expense_total'] >= 0
                    # loan
                    else self.INFLATION / 12,
                    12,
                    currnet_row['income_total'] + currnet_row['expense_total']
                )
                previous_saving_with_interest_pv = -self.pv(
                    self.INFLATION,
                    1,
                    0,
                    previous_saving_with_interest
                )
                income_with_interest_pv = -self.pv(
                    self.INFLATION,
                    1,
                    0,
                    income_with_interest
                )
                current_saving = previous_saving_with_interest_pv + income_with_interest_pv
                income_portfolio = previous_saving_with_interest_pv - previous_saving
                previous_saving = current_saving
                return income_portfolio, current_saving

        df[['income_portfolio_annually', 'saving']] = df.agg(
            cal__saving,
            axis=1
        )

        if not detail:
            df.drop(columns='income_portfolio_annually', axis=1, inplace=True)

    @staticmethod
    def cal__financial_independence(df):
        df['financial_independence'] = df.apply(
            lambda x: 'SUCCESS'
            if x['income_portfolio_annually'] + x['expense_total'] * 12 >= 0
            else '-',
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

        self.cal__saving(df, detail)

        detail and self.cal__financial_independence(df)

        return df

    def optimize(self):
        """
        https://stackoverflow.com/a/52839257/11169132
        https://blog.csdn.net/qq_40707407/article/details/81709122
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

        Constraints:

            1. saving >= 0
            2. min(last saving)
            3. RATE_YEARLY_GROWTH_SALARY >= self.INFLATION
            4. RATE_YEARLY_GROWTH_PORTFOLIO >= self.INFLATION
            # 5. 0 <= max_income_monthly <= current income

        :return:
        """

        def constraints(xk):
            rate = xk[0]
            self.RATE_YEARLY_GROWTH_SALARY = self.RATE_YEARLY_GROWTH_PORTFOLIO = rate
            df = self.build_data(detail=False)
            last_saving = df.loc[df['year'] == self.date_of_death.year, 'saving']
            self.last_saving = last_saving
            return self.last_saving

        # noinspection PyTypeChecker
        res = optimize.minimize(
            lambda _: self.last_saving,
            x0=np.array([self.INFLATION]),
            method='COBYLA',
            options={
                # https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html#minimize-method-cobyla
                # initial step to change that variables
                'rhobeg': 0.05,
                'maxiter': 300,
                # Tolerance (absolute) for constraint violations
                'catol': 0.05,
                # Final accuracy in the optimization
                'tol': 0.0000001,
            },
            constraints=(
                # `eq` constraint means that the constraint function result is to be zero
                # `ineq` means that it is to be non-negative
                {'type': 'ineq', 'fun': constraints},
                {'type': 'ineq', 'fun': lambda x: x[0] - self.INFLATION},
                {'type': 'ineq', 'fun': lambda x: 0.2 - x[0]},
            ),
        )
        return res

    def build__assumptions_df(self):
        # noinspection PyTypeChecker
        assumptions = pd.DataFrame(
            [
                {
                    attr: getattr(self, attr)
                    for attr in sorted(dir(self))
                    if not isinstance(getattr(self, attr), Callable)
                       and not attr.startswith('__')
                       and not attr in {
                    'last_saving',
                }
                }
            ]
        )
        assumptions = assumptions.transpose().reset_index()
        return assumptions

    @staticmethod
    def set__column_width(df, writer, sheet):
        for column in df:
            column_length = max(
                df[column].astype(str).map(len).max(),
                len(column)
                if isinstance(column, str)
                else 0
            )
            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet].set_column(col_idx, col_idx, column_length + 1)

    @staticmethod
    def set__column_format(
            writer,
            sheet,
            num_format,
            columns='F:ZZ',

    ):
        worksheet = writer.sheets[sheet]
        worksheet.set_column(columns, None, num_format)

    def build__report(
            self,
            report_name=Path(__file__).parents[1].joinpath(
                f'Retirement-{datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}-report.xlsx'
            ).absolute(),
            note='',
            detail=False
    ):
        """
        write excel sheets of:

        1. attribute
        2. balance sheet
        3. expense cashflow
        3. income cashflow

        """
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(
            report_name,
            engine='xlsxwriter'
        )
        self.note = note
        # build DataFrames
        df_attrs = self.build__assumptions_df()
        time_scale = range(self.date_of_work.year, self.date_of_death.year + 1)
        df_timeframe = self.build__df_time_frame(time_scale)
        df_expense = self.build__df_expense(time_scale)
        df_income = self.build__df_income(time_scale)
        df_expense = df_timeframe.merge(df_expense, on='year')
        df_income = df_timeframe.merge(df_income, on='year')
        df = self.build_data(detail=detail)

        # write DataFrames to excel sheets
        df_attrs.to_excel(
            writer,
            sheet_name='Assumptions',
            index=False,
            header=False
        )
        df_expense.to_excel(
            writer,
            sheet_name='Expense Cash Flow',
            index=False,
        )
        df_income.to_excel(
            writer,
            sheet_name='Income Statement',
            index=False,
        )
        df.to_excel(
            writer,
            sheet_name='Balance Sheet',
            index=False,
        )

        # set columns format
        workbook = writer.book
        num_format = workbook.add_format({'num_format': '#,##0.00', })
        self.set__column_format(writer, 'Assumptions', num_format, "A:B")
        self.set__column_format(writer, 'Expense Cash Flow', num_format)
        self.set__column_format(writer, 'Income Statement', num_format)
        self.set__column_format(writer, 'Balance Sheet', num_format)

        # set column width
        self.set__column_width(df_attrs, writer, 'Assumptions')
        self.set__column_width(df_expense, writer, 'Expense Cash Flow')
        self.set__column_width(df_income, writer, 'Income Statement')
        self.set__column_width(df, writer, 'Balance Sheet')

        # close and save file
        writer.save()
        print(f"Report wrote to {report_name}")


if __name__ == '__main__':
    from .utils import df2excel

    # pass ur own data
    import env_202207 as env

    plan = Retirement(
        env.date_of_money_value,
        env.date_of_birth,
        env.date_of_birth_spouse,
        env.date_of_birth_child,
        env.date_of_birth_parents,
        env.date_of_work,
        env.date_of_work_spouse,
        env.age_of_wedding,
        env.age_of_car,
        env.age_of_housing,
        env.price_per_square,
        env.area,
        env.price_per_decoration,
        env.age_of_nursing,
        env.expense_monthly_single_nursing,
        env.age_of_retirement,
        env.expense_monthly_pension_couple,
        env.income_monthly,
        env.saving,
        env.income_monthly_spouse,
        env.max_income_monthly,
        env.expense_monthly_food,
        env.max_expense_monthly_food,
        env.expense_monthly_renting,
        env.max_expense_monthly_renting,
        env.expense_monthly_recreation,
        env.max_expense_monthly_recreation,
        env.expense_wedding,
        env.expense_car,
    )

    otires = plan.optimize()
    print(otires)
    if not otires.success:
        print(
            '\nSorry, the algorithm cannot find a reasonable solution\n'
            'Please lower the expense or higher the income'
        )
        exit()

    plan.RATE_YEARLY_GROWTH_PORTFOLIO = plan.RATE_YEARLY_GROWTH_SALARY = otires.x[0]
    # retirement_df = plan.build_data(
    #     detail=True
    # )
    # df2excel(
    #     df=retirement_df,
    #     file_name=f'../retirement-{datetime.datetime.today().strftime("%Y-%m-%d")}.xlsx',
    #     num_format_column='F:ZZ'
    # )
    plan.build__report(
        detail=True,
        note='working in the U.S. after 2 years of graduate studying. \n'
             'pay attention to the max_income_monthly '
    )
