#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm



def pv(__rate, __nper, __pmt=0, __fv=0, __type=0):
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


def fv(__rate, __nper, __pmt=0, __pv=0, __type=0):
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


def pmt(__rate, __nper, __pv=0, __fv=0, __type=0):
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


if __name__ == '__main__':
    pass