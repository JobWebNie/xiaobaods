#!/usr/bin/env python
# -*- coding: gbk -*-

"""
__title__ = ''
__author__ = 'Administrator'
__mtime__ = '2017-10-09'
"""
import initialize
import function


def get_argv():
    argv = {}
    if __name__ == '__main__':
        try:
            import sys
            argv = sys.argv[1]
            argv = eval(argv)
        except:
            argv = {}
    return argv


def console(argv, debug=0):
    SQL_msg = initialize.conftodict("xiaobaods_SQL.conf")
    if debug == 8:
        argv["debug"] = 8
    # storegroup = initialize.storegrouplist('storegroup.txt')
    if argv.get("fun") == "a" or argv.get("fun") == None:
        df = function.xiaobaods_a(SQL_msg=SQL_msg, line_b=argv.get("line_b", 0), line_f=argv.get("line_f", 20),
        date=argv.get("date", ""), category=argv.get("category", "牛仔裤"), length=argv.get("length", 7),
        SQL=argv.get("SQL", "xiaobaods"), table=argv.get("table", "bc_attribute_granularity_sales"),
        variable=argv.get("variable", "热销排名"), debug=argv.get("debug", 0), fillna=argv.get("fillna", ""),
        path=argv.get("path", ""), keyword=argv.get("keyword", "日期："), rankl=argv.get("rankl", 0), rankm=argv.get("rankm", 0),
        titler=argv.get("titler", ""), storer=argv.get("storer", ""), v1l=argv.get("v1l", 0), v1m=argv.get("v1m", 0),
        v2l=argv.get("v2l", 0), v2m=argv.get("v2m", 0), v3l=argv.get("v3l", 0), v3m=argv.get("v3m", 0))
    return df


def view():
    df = console(get_argv(), debug=8)
    print(df)


console(get_argv())

