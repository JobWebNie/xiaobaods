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
fc.xiaobaods_ws(df_raw=fc.xiaobaods_w(date=argv.get("date",""),category=argv.get("category","ţ�п�"),length=argv.get("length",7),SQL=argv.get("SQL","xiaobaods"),choice=argv.get("choice","���Ѻ��Ĵ�"),variable=argv.get("variable","����"),fillna=argv.get("fillna",""),debug=8),df_sort=fc.xiaobaods_w(date=argv.get("date",""),category=argv.get("category","ţ�п�"),length=argv.get("length",7),SQL=argv.get("SQL","xiaobaods"),choice=argv.get("choice","���Ѻ��Ĵ�"),variable="����",fillna=500,debug=8),algorithm=argv.get("algorithm",1),alpha=argv.get("alpha",""),head=argv.get("head",5),debug=argv.get("debug",""),path=argv.get("path",""))