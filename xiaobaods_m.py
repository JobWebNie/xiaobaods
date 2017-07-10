#!usr/bin/env python3
#! -*- coding: gbk -*-
import xiaobaods_function as fc
if __name__ == "__main__":
    try:
        import sys
        argv = sys.argv[1]
        argv = eval(argv)
    except:
        argv ={}
# us function m
fc.xiaobaods_m(date=argv.get("date",""),SQL=argv.get("SQL","xiaobaods"),category=argv.get("category","??×???"),display=argv.get("display","year"),vs=argv.get("vs","onyear"),variable=argv.get("variable","all"),debug=argv.get("debug",0),path=argv.get("path",""))
