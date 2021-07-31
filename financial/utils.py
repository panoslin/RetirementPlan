#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/10
# IDE: PyCharm
import datetime
import time
import pandas as pd
from pathlib import Path
from typing import Union


def str2datetime(x: Union[str, datetime.date, datetime.datetime]):
    return datetime.datetime.fromtimestamp(
        time.mktime(
            time.strptime(
                x,
                '%Y/%m/%d'
            )
        )
    ) if isinstance(x, str) else x


def df2excel(
        df,
        file_name=Path(__file__).parent.joinpath(
            f'retirement-{datetime.datetime.today().strftime("%Y-%m-%d")}.xlsx'
        ).absolute(),
        num_format_column='F:R'

):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(
        file_name,
        engine='xlsxwriter'
    )
    df.to_excel(
        writer,
        index=False,
    )
    # set columns format
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '#,##0'})
    worksheet.set_column(num_format_column, None, format1)
    # set column width
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length + 1)
    # close and save file
    writer.save()


if __name__ == '__main__':
    pass
