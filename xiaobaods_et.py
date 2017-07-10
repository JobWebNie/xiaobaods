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
# us function et
fc.xiaobaods_et(SQL=argv.get("SQL","xiaobaods"),category=argv.get("category","牛仔裤"),attribute=argv.get("attribute","腰型"),feature=argv.get("feature",""),variable=argv.get("variable","all"),stats=argv.get("stats",""),debug=argv.get("debug",""),path=argv.get("path",""))
