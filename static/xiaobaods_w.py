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
# us function ws
fc.xiaobaods_w(date=argv.get("date",""),category=argv.get("category","ţ�п�"),length=argv.get("length",7),SQL=argv.get("SQL","xiaobaods"),choice=argv.get("choice","���Ѻ��Ĵ�"),variable=argv.get("variable","����"),fillna=argv.get("fillna",""),debug=argv.get("debug",""),path=argv.get("path",""))