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
# us function e
fc.xiaobaods_e(date=argv.get("date",""),category=argv.get("category","ţ�п�"),SQL=argv.get("SQL","xiaobaods"),attribute=argv.get("attribute",""),variable=argv.get("variable","�ɽ���"),debug=argv.get("debug",""),path=argv.get("path",""))