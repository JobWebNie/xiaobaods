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
fc.xiaobaods_c(date=argv.get("date",""),category=argv.get("category","ţ�п�"),classification=argv.get("classification","��ʽ"),attributes=argv.get("attributes","Ǧ�ʿ�"),length=argv.get("length",7),SQL=argv.get("SQL","xiaobaods"),variable=argv.get("variable","��������"),debug=argv.get("debug",0),fillna=argv.get("fillna",""),path=argv.get("path",""),keyword=argv.get("keyword","���ڣ�"),storechoice=argv.get("storechoice",""),storegroupchoice=argv.get("storegroupchoice",""))