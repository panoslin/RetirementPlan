#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
import datetime
import time

str2datetime = lambda x: datetime.datetime.fromtimestamp(
    time.mktime(
        time.strptime(
            x,
            '%Y/%m/%d'
        )
    )
)

if __name__ == '__main__':
    pass