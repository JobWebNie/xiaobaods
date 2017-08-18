#!usr/bin/env python3
#! -*- coding: utf-8 -*-
import xiaobaods_function as fc
if __name__ == "__main__":
    try:
        import sys
        argv = sys.argv[1]
        argv = eval(argv)
    except:
        argv ={}
fc.xiaobaods_a(date=argv.get("date",""),category=argv.get("category","牛仔裤"),length=argv.get("length",7),SQL=argv.get("SQL","xiaobaods"),table=argv.get("table","bc_attribute_granularity_sales"),variable=argv.get("variable","热销排名"),debug=argv.get("debug",0),fillna=argv.get("fillna",""),path=argv.get("path",""),keyword=argv.get("keyword","日期："),titlechoice=argv.get("titlechoice",""),storechoice=argv.get("storechoice",""),storegroupchoice=argv.get("storegroupchoice",""))