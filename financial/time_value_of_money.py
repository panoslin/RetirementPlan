#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
"""
Reference:

https://github.com/microsoft/referencesource/blob/master/Microsoft.VisualBasic/runtime/msvbalib/Financial.vb

"""

import datetime

nper = lambda x: x - datetime.datetime.now().year


def pv(
        __rate: float,
        __nper: int,
        __pmt: float = 0,
        __fv: float = 0,
        __type: bool = 0
):
    """
    Calculate the present value

         -fv - PMT * (1+rate*type) * ( (1+rate)^nper-1) / rate
    pv = -----------------------------------------------------
                       (1 + rate) ^ nper

    pv = -fv - PMT * nper     : if rate == 0

    :return:
    """
    if __rate == 0:
        return -__fv - __pmt * __nper
    else:
        return (
                       -__fv
                       - __pmt * (1 + __rate * __type) * ((1 + __rate) ** __nper - 1) / __rate
               ) / (1 + __rate) ** __nper


def fv(
        __rate: float,
        __nper: int,
        __pmt: float = 0,
        __pv: float = 0,
        __type: bool = 0
) -> float:
    """
    Calculate the future value

                                               (1+rate)^nper - 1
    fv = -pv*(1+rate)^nper - PMT*(1+rate*type)* -----------------
                                                     rate

    fv = -pv - PMT * nper        : if rate == 0

    """
    if __rate == 0:
        return -__pv - __pmt * __nper
    else:
        return -__pv * (1 + __rate) ** __nper \
               - __pmt * (1 + __rate * __type) \
               * (
                       ((1 + __rate) ** __nper - 1)
                       / __rate
               )


def pmt(
        __rate: float,
        __nper: int,
        __pv: float = 0,
        __fv: float = 0,
        __type: bool = 0
):
    """
    Calculate the regular payment

          (-fv - pv*(1+rate)^nper) * rate
    PMT = -------------------------------------
          (1+rate*type) * ( (1+rate)^nper - 1 )

    PMT = (-fv - pv) / nper    : if rate == 0

    """
    if __rate == 0:
        return (-__fv - __pv) / __nper
    else:
        return (
                       (-__fv - __pv * (1 + __rate) ** __nper) * __rate
               ) / ((1 + __rate * __type) * ((1 + __rate) ** __nper - 1))


def pmt_with_down_pmt(
        year,
        start_year,
        end_year,
        loan_rate,
        down_pmt_percentage,
        amount,

):
    """
    return the month payment along with the down payment if any
    :param year:
    :param start_year:
    :param end_year:
    :param loan_rate:
    :param down_pmt_percentage:
    :param amount:
    :return:
    """
    if start_year <= year < end_year:
        regular_pmt = pmt(
            loan_rate / 12,
            (end_year - start_year) * 12,
            (1 - down_pmt_percentage) * amount
        )
        down_pmt = -amount * down_pmt_percentage / 12 if year == start_year else 0
        return regular_pmt + down_pmt
    else:
        return 0


if __name__ == '__main__':
    pass
