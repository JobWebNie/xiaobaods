#!usr/bin/env python3
# -*- coding: gbk -*-
import sys,os
import xiaobaods_function as fc
import pandas as pd
import datetime
def analysis_ws(date="",length=15,SQL="xiaobaods",fillna="",head=5,algorithm=1):
    df = pd.DataFrame()
    for category in ["牛仔裤","打底裤","休闲裤"]:
        dic = {}
        for choice_list in ["热搜修饰词","热搜品牌词","热搜搜索词","热搜核心词","热搜长尾词"]:
            dic[choice_list]={}
            msg = list(fc.xiaobaods_ws(df_raw= fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=8,variable="排名",fillna=fillna,category=category,choice=choice_list),
                    df_sort=fc.xiaobaods_w(date=date,length=length,SQL=SQL,fillna=500,variable="排名",debug=8,category=category,choice=choice_list),
                    debug=8,algorithm=algorithm,head=head)["搜索词"])
            for i in range(head):
                dic[choice_list][i] = msg[i]
        df1 = pd.DataFrame(dic).T
        df1["类别"] = category
        try:
            df = pd.concat([df,df1])
        except:
            df = df1.copy()
    df.set_index(["类别"],inplace=True,append=True)
    df.index = df.index.swaplevel()
    df.index.names = ["类别","表单"]
    df.columns = ["Top"+str(n+1) for n in range(head)]
    info = fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=7,variable="排名",fillna=fillna,category=category,choice=choice_list)
    df.columns.names = [info["date"].replace("-","")[len(info["date"].split("-")[0]):]+"[:"+info["length"]+"]"]
    return df
def analysis_wl(date="",length=15,datelist=7,interval=1,SQL="xiaobaods",fillna="",head=5,algorithm=1,category="牛仔裤",choice="热搜修饰词"):
    df = pd.DataFrame()
    if category not in ["牛仔裤","打底裤","休闲裤"]:
        category = "牛仔裤"
    if choice not in ["热搜修饰词","热搜品牌词","热搜搜索词","热搜核心词","热搜长尾词"]:
        choice = "热搜修饰词"
    if datelist < 0:
        datelist = 7
    interval = int(interval)
    if interval < 0 or interval > 7:
        interval = 1
    dic = {}
    for i in range(datelist):
        date=datetime.datetime.strftime(datetime.datetime.today().date()-datetime.timedelta(1+i*interval),"%Y-%m-%d")
        dic[date] = {}
        msg = list(fc.xiaobaods_ws(df_raw= fc.xiaobaods_w(date=date,length=length,SQL=SQL,debug=8,fillna=fillna,category=category,choice=choice),
                    df_sort=fc.xiaobaods_w(date=date,length=length,SQL=SQL,fillna=500,variable="排名",debug=8,category=category,choice=choice),
                    debug=8,algorithm=algorithm,head=head)["搜索词"])
        for i in range(head):
            dic[date][i] = msg[i]
    df = pd.DataFrame(dic).T
    df.sort_index(inplace=True,ascending=True)
    df.columns = ["Top"+str(n+1) for n in range(head)]
    df.columns.names = [category+"["+choice+"]"]
    df.index.names = ["EDT.Sort"]
    return df.T