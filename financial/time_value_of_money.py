#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
"""
Reference:

https://github.com/microsoft/referencesource/blob/master/Microsoft.VisualBasic/runtime/msvbalib/Financial.vb

"""

import datetime


class TimeValue:
    @classmethod
    def nper(cls, year):
        return year - datetime.datetime.now().year

    @classmethod
    def pv(cls,
           rate: float,
           nper: int,
           pmt: float = 0,
           fv: float = 0,
           xtype: bool = 0
           ):
        """
        Calculate the present value
    
             -fv - PMT * (1+rate*type) * ( (1+rate)^nper-1) / rate
        pv = -----------------------------------------------------
                           (1 + rate) ^ nper
    
        pv = -fv - PMT * nper     : if rate == 0
    
        :return:
        """
        if rate == 0:
            return -fv - pmt * nper
        else:
            return (
                           -fv
                           - pmt * (1 + rate * xtype) * ((1 + rate) ** nper - 1) / rate
                   ) / (1 + rate) ** nper

    @classmethod
    def fv(
            cls,
            rate: float,
            nper: int,
            pmt: float = 0,
            pv: float = 0,
            xtype: bool = 0
    ) -> float:
        """
        Calculate the future value
    
                                                   (1+rate)^nper - 1
        fv = -pv*(1+rate)^nper - PMT*(1+rate*type)* -----------------
                                                         rate
    
        fv = -pv - PMT * nper        : if rate == 0
    
        """
        if rate == 0:
            return -pv - pmt * nper
        else:
            return -pv * (1 + rate) ** nper \
                   - pmt * (1 + rate * xtype) \
                   * (
                           ((1 + rate) ** nper - 1)
                           / rate
                   )

    @classmethod
    def pmt(
            cls,
            rate: float,
            nper: int,
            pv: float = 0,
            fv: float = 0,
            xtype: bool = 0
    ):
        """
        Calculate the regular payment
    
              (-fv - pv*(1+rate)^nper) * rate
        PMT = -------------------------------------
              (1+rate*type) * ( (1+rate)^nper - 1 )
    
        PMT = (-fv - pv) / nper    : if rate == 0
    
        """
        if rate == 0:
            return (-fv - pv) / nper
        else:
            return (
                           (-fv - pv * (1 + rate) ** nper) * rate
                   ) / ((1 + rate * xtype) * ((1 + rate) ** nper - 1))

    @classmethod
    def pmt_with_down_pmt(
            cls,
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
            regular_pmt = cls.pmt(
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
